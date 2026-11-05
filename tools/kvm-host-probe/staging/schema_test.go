package staging

import (
	"encoding/json"
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
)

func TestStageReceiptSchemaMatchesGoWireFields(t *testing.T) {
	data, err := os.ReadFile(filepath.Join("..", "schemas", "stage-result.v1.schema.json"))
	if err != nil {
		t.Fatal(err)
	}
	var schema struct {
		ID                   string                     `json:"$id"`
		Type                 string                     `json:"type"`
		AdditionalProperties bool                       `json:"additionalProperties"`
		Required             []string                   `json:"required"`
		Properties           map[string]json.RawMessage `json:"properties"`
	}
	if err := json.Unmarshal(data, &schema); err != nil {
		t.Fatal(err)
	}
	if schema.ID != "urn:forgepanel:r3:kvm-image-stage:result:v1" || schema.Type != "object" || schema.AdditionalProperties {
		t.Fatalf("unexpected schema identity %+v", schema)
	}
	expected := map[string]bool{}
	typ := reflect.TypeOf(Result{})
	for i := 0; i < typ.NumField(); i++ {
		name := strings.Split(typ.Field(i).Tag.Get("json"), ",")[0]
		if name == "" || name == "-" {
			t.Fatalf("unmapped field %s", typ.Field(i).Name)
		}
		expected[name] = true
	}
	if len(expected) != len(schema.Properties) {
		t.Fatalf("fields diverged: struct=%d schema=%d", len(expected), len(schema.Properties))
	}
	for name := range expected {
		if _, ok := schema.Properties[name]; !ok {
			t.Fatalf("missing schema field %s", name)
		}
	}
	for _, name := range schema.Required {
		if !expected[name] {
			t.Fatalf("unknown required field %s", name)
		}
	}
}
func TestStageSchemaForbidsExecutionAndFakeImmutability(t *testing.T) {
	data, err := os.ReadFile(filepath.Join("..", "schemas", "stage-result.v1.schema.json"))
	if err != nil {
		t.Fatal(err)
	}
	var doc struct {
		Properties map[string]map[string]any `json:"properties"`
	}
	if err := json.Unmarshal(data, &doc); err != nil {
		t.Fatal(err)
	}
	for _, field := range []string{"execution_authorized", "immutable_storage_verified", "resource_quotas_enforced", "vm_executed", "report_signed"} {
		if value, ok := doc.Properties[field]["const"]; !ok || value != false {
			t.Fatalf("false assertion possible in %s", field)
		}
	}
	if doc.Properties["qualification"]["const"] != "NOT_EXECUTED" {
		t.Fatal("qualification not forced to NOT_EXECUTED")
	}
	if doc.Properties["manual_review_required"]["const"] != true {
		t.Fatal("manual review not forced")
	}
}
