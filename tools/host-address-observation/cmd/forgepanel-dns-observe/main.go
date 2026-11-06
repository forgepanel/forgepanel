// Explicitly invoked DNS observation of the machine's own FQDN.
// This does not establish public DNS authority, TLS or reachability.
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"github.com/yyogas/forgepanel/tools/host-address-observation/observer"
)

func main() {
	if len(os.Args) != 2 || os.Args[1] != "--observe" {
		fmt.Fprintln(os.Stderr, "usage: forgepanel-dns-observe --observe (OS resolver lookup for this machine only)")
		os.Exit(2)
	}
	report := observer.InspectResolver(context.Background(), observer.InspectHost(), observer.OSResolver{})
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(report); err != nil {
		fmt.Fprintln(os.Stderr, "failed to encode resolver observation")
		os.Exit(1)
	}
}
