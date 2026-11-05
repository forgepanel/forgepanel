package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/yyogas/forgepanel/tools/kvm-host-probe/probe"
)

func main() {
	// No input paths or commands are accepted by this unprivileged inspector.
	if len(os.Args) != 1 {
		fmt.Fprintln(os.Stderr, "usage: forgepanel-kvm-probe (no arguments)")
		os.Exit(2)
	}
	report := probe.InspectHost()
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(report); err != nil {
		fmt.Fprintln(os.Stderr, "failed to encode host observation")
		os.Exit(1)
	}
}
