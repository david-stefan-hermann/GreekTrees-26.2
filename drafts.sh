#!/bin/bash
# Draft rounds of PLAN-PALME-WEIDE.md: ./drafts.sh p1 w1 -> concept/drafts_p1.png, concept/drafts_w1.png
cd "$(dirname "$0")" || exit 1
export MSYS_NO_PATHCONV=1 JAVA_HOME='C:\Program Files\Eclipse Adoptium\jdk-25.0.4.101-hotspot' TEMP='C:\jtmp' TMP='C:\jtmp'
rounds=$(IFS=,; echo "$*")
./gradlew runServer -Pdrafts="$rounds" -q > drafts.out 2>&1
grep -E "Fehler|error:|FAILED|greektrees-drafts|Exception in|loopback" drafts.out
cd concept && python render_selftest.py drafts "$@"
