// A non-privileged, read-only Linux host capability hint observer.
package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/yyogas/forgepanel/tools/app-center-host-probe/probe"
)

func main() {
	if len(os.Args) != 1 {
		fmt.Fprintln(os.Stderr, "usage: forgepanel-app-center-observe (no arguments)")
		os.Exit(2)
	}
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	if err := enc.Encode(probe.InspectHost()); err != nil {
		fmt.Fprintln(os.Stderr, "failed to encode host observation")
		os.Exit(1)
	}
}
