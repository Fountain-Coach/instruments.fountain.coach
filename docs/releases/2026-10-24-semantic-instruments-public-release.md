# Instruments — semantic icon edition publicly released

**Date:** 24 October 2026. **User authorization:** Following "should we deploy now?", user explicitly corrected release scope to "instruments !". The bounded intended effect is the existing instruments.fountain.coach public static site, not Book, Works or Status.

## Source and editorial provenance

Source owner: Fountain-Coach/instruments.fountain.coach. Source Git revision: `5ac718ed67bd9d528a294d3d4e94ef2514efd67e`. The published Instruments front page exposes Sing, Ear and SatzfunkPlayer as separately developing musical/semantic capabilities without claiming all three are certified MIDI 2.0 hardware instruments. The author's accepted logo correction reuses the standard Lucide microphone, ear and clapperboard glyph paths, version 0.468.0, with the ISC license retained and supplied publicly as `/assets/lucide-isc-license.txt`.

Canonical owner-WLAN staging's Instruments page was accepted as the candidate at v21, retained byte-identical in the v26 combined staging release. The authored page main text matches that staged semantic entrance. Production-specific transformation preserved the verified public 9-entry reel, Status legal/footer link and whole footer; rewrote only stage-only /instruments/assets paths to exact-host /assets. The existing three historical Codex Login, Semantic Browser and Csound AUv3 HTML routes remain identical to the predecessor.

## Publication host and production-first lineage

Exact public host: `https://instruments.fountain.coach/`. Owner's existing Hetzner Caddy static release root: `/srv/fountain-static-publications/instruments.fountain.coach/`. Independently verified predecessor: `releases/estate-20261024-v14-satzfunk-reel-instruments`. Local release candidate was assembled as that full observed production baseline plus the owner's Git-authorized Instruments revision, the source-owned supporting assets, and ISC license.

Original predecessor contained 11 files. The candidate contains 30 files: only `index.html` and `assets/site.css` changed, 19 supporting assets added; all three published historical deep HTML pages and existing shared shell assets were preserved byte-for-byte. Production baseline index, stylesheet and all three deep pages were matched independently with public HTTPS SHA-256 before attempting promotion.

The new release was prepared and preflighted by the preinstalled typed `EstatePublisherSSHDelivery` client, configured for the exact host and existing owner SSH, with SHA-256 file manifest. No additional remote publisher, SSH credential, token, CI job or DNS origin was installed.

## First attempted publication and observed real defect

The first exact-host delivery, `estate-20261024-v15-semantic-instruments-5ac718e`, **activated**, verified the new homepage, then saw a SHA-256 mismatch at `/assets/site.css`. The native publisher invoked rollback to v14 (receipt state `rollbackAcknowledgedUnverified`). Subsequent independent SSH and public HTTPS checks showed v14 again active and old homepage and stylesheet bytes restored. The first typed receipt is kept at [2026-10-24-instruments-v15-rolled-back-receipt.json](2026-10-24-instruments-v15-rolled-back-receipt.json).

The real cause was the existing `/etc/caddy/Caddyfile` matcher `@estateRailInstruments`: its path list included only the Instruments homepage, three deep pages and fingerprinted shared-shell assets; **it omitted `/assets/site.css` and all Instruments-owned semantic icon/social assets**. Those requests therefore fell through to an older reverse-proxy publication path even while the homepage was correctly served from the new release symlink. This is a demonstrated asset-routing defect, not a reason to invent a new publication mechanism.

The minimal corrective change was appending the single Caddy matcher pattern `/assets/*` to the existing `@estateRailInstruments` path line. It remains host-scoped to `instruments.fountain.coach`; no other matchers, Caddy roots, TLS identities, services or DNS were changed. `caddy validate` passed before applying and `systemctl reload caddy` succeeded. Original config backup: `/etc/caddy/Caddyfile.before-instruments-assets-20261024`. Original Caddyfile SHA-256 `8c001a5929cd3f2033b7679cea9ae09c1ac37d1b83318eb9d1bef55ca18d7e1d`; accepted Caddyfile SHA-256 `bc2e60820fe9d77ee875a688e3c7a46a573bd2619be28c2e4db1292f4c5126cc`.

## Successful typed release and independent witnesses

The same immutable 30-file candidate was reissued under a new release identity, **`estate-20261024-v16-instruments-assets-5ac718e`**, with declared predecessor v14 and unchanged source Git SHA. Native EstatePublisher's new complete manifest, [2026-10-24-instruments-v16-manifest.json](2026-10-24-instruments-v16-manifest.json), passed preflight. [The typed public release receipt](2026-10-24-instruments-v16-public-receipt.json) reports `state=active` and seven exact HTTPS SHA-256 witnesses, all matched:

- Homepage `/index.html`: `68f654280e64b15b0c1c04585b47c05c0b1a067bc95112d55c261786ace18d4d`
- Style `/assets/site.css`: `bad09263355e590adfe73d975828e3e08a2067cc5a4afa275b19f2c1877145fc`
- Sing microphone: `ad2b3766d5dd8f83f8d8eb0047d81717a3a624195fa2e81ff2e59a68ff064a29`
- Ear: `59987946969574248eb6fe94518ed1555644582c03be7ff3f308c63224c93b31`
- SatzfunkPlayer clapperboard: `869662c633d086ebce56a504fb51eae9ab82daff4d6c5e57903e1b6eb1eebf32`
- Social PNG: `96868e1c2240a4cfe892f58233f18c22af17375cf8c4a80ad0cc8a85dfb0171e`
- Preserved Codex Login historical document: `56a65da13f63a2c8c568e9d8f9ecfcfe92bafd0f69b02fcfab8018893d1a11a0`

Independent follow-up HTTP verification confirmed these and both other preserved historic routes byte-for-byte. Live production symlink points to `releases/estate-20261024-v16-instruments-assets-5ac718e` with the original v14 and inert rolled-back v15 candidate retained. Caddy service was observed active.

Local Chromium independently loaded the actual new HTTPS site at desktop 1280 x 900 and phone 393 x 852, with browser cache disabled. Both showed Sing/Ear/SatzfunkPlayer standard icons, 9 correct top-level entries (including Satzfunk, excluding Status), Status footer link, all three historical document links, no missing images, no JavaScript errors and no horizontal overflow. Local screenshots retained privately as publication witness; native macOS Safari/iPad parity not claimed.

Book production remained at `releases/estate-20261024-v14-satzfunk-reel-book`, WLAN combined staging remained `shared-shell-20261024-v26-discreet-references-876b613`, and public Book, Works and Status routes remained available. This is **only** the Instruments promotion. No private documents or other staged changes were released.

## Follow-through

The source owner controls the public Instruments site and this exact-host release receipt. Any future Caddyfile regeneration must carry the one-host asset matcher change rather than restore the older nonmatching fallback. The receipt, immutable release and backed-up Caddyfile provide rollback evidence. This publication does not certify other instrument runtime/physical acceptance.
