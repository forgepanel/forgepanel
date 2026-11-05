package admission

import (
	"encoding/json"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
)

type schemaShape struct {
	Schema string `json:"$schema"`
	ID string `json:"$id"`
	Type string `json:"type"`
	AdditionalProperties bool `json:"additionalProperties"`
	Required []string `json:"required"`
	Properties map[string]json.RawMessage `json:"properties"`
}

func TestVersionedJSONSchemasMatchGoWireFields(t *testing.T) {
	cases := []struct {
		file string
		object any
		mustAllRequired bool
	}{
		{"policy.v1.schema.json", Policy{}, true},
		{"request.v1.schema.json", Request{}, true},
		{"result.v1.schema.json", Result{}, false},
	}
	for _, testCase := range cases {
		t.Run(testCase.file, func(t *testing.T) {
			data, err := os.ReadFile(filepath.Join("..", "schemas", testCase.file))
			if err != nil { t.Fatal(err) }
			var schema schemaShape
			if err := json.Unmarshal(data, &schema); err != nil { t.Fatal(err) }
			if schema.Schema != "https://json-schema.org/draft/2020-12/schema" ||
				!strings.HasPrefix(schema.ID, "urn:forgepanel:r3:kvm-image-admission:") || schema.Type != "object" || schema.AdditionalProperties {
				t.Fatalf("invalid schema metadata: %+v", schema)
			}
			fields := reflect.TypeOf(testCase.object)
			actual := map[string]bool{}
			for i := 0; i < fields.NumField(); i++ {
				name := strings.Split(fields.Field(i).Tag.Get("json"), ",")[0]
				if name == "" || name == "-" { t.Fatalf("field without JSON contract: %s", fields.Field(i).Name) }
				actual[name] = true
			}
			if len(actual) != len(schema.Properties) { t.Fatalf("wire fields out of sync: go=%v schema=%v", actual, schema.Properties) }
			for name := range actual {
				if _, ok := schema.Properties[name]; !ok { t.Fatalf("schema missing Go JSON field %s", name) }
			}
			required := map[string]bool{}
			for _, name := range schema.Required {
				if required[name] { t.Fatalf("duplicate required field %s", name) }
				required[name] = true
				if !actual[name] { t.Fatalf("required field does not exist %s", name) }
			}
			if testCase.mustAllRequired && len(required) != len(actual) {
				t.Fatalf("missing required fields: %d vs %d", len(required), len(actual))
			}
		})
	}
}

func TestResultSchemaForbidsFalseQualificationClaims(t *testing.T) {
	data, err := os.ReadFile(filepath.Join("..", "schemas", "result.v1.schema.json"))
	if err != nil { t.Fatal(err) }
	var schema struct{ Properties map[string]map[string]any `json:"properties"` }
	if err := json.Unmarshal(data, &schema); err != nil { t.Fatal(err) }
	for _, field := range []string{"vm_executed", "runner_isolated", "resource_quotas_enforced", "image_format_fully_validated", "report_signed", "q132_security_gates_passed"} {
		if v, ok := schema.Properties[field]["const"]; !ok || v != false {
			t.Fatalf("schema permits fake success: %s", field)
		}
	}
	if schema.Properties["qualification"]["const"] != "NOT_EXECUTED" {
		t.Fatal("qualification contract changed")
	}
}
