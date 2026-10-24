#!/usr/bin/env python3
"""One static, source-owned Instruments editorial delta; never a runtime renderer."""
from pathlib import Path
import argparse, re, shutil

LOGOS = {
"sing": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title desc"><title id="title">Sing — voice and articulation</title><desc id="desc">A vertical vocal source with three open resonating waves</desc><rect width="256" height="256" rx="48" fill="#eceee7"/><g fill="none" stroke="#283733" stroke-linecap="round" stroke-linejoin="round"><path d="M128 184V73" stroke-width="11"/><path d="M113 73a15 15 0 0 1 30 0" stroke-width="10"/><path d="M97 96c-21 15-21 49 0 64m62-64c21 15 21 49 0 64" stroke-width="8"/><path d="M71 77c-33 27-33 76 0 103m114-103c33 27 33 76 0 103" stroke-width="7"/><path d="M105 188h46" stroke-width="7"/></g><circle cx="128" cy="57" r="7" fill="#a07755"/></svg>""",
"ear": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title desc"><title id="title">Ear — attentive listening</title><desc id="desc">Three arriving sound arcs converge at a listening point</desc><rect width="256" height="256" rx="48" fill="#eceee7"/><g fill="none" stroke="#283733" stroke-linecap="round"><path d="M72 69c-35 31-36 89-3 122" stroke-width="7"/><path d="M100 87c-24 23-25 58-1 82" stroke-width="8"/><path d="M132 106c-11 10-11 31 0 42" stroke-width="9"/><path d="M157 58c34 15 56 47 56 84 0 36-19 61-52 76" stroke-width="7"/><path d="M158 89c19 10 30 27 30 48 0 20-10 35-29 44" stroke-width="7"/></g><circle cx="150" cy="128" r="11" fill="#a07755"/></svg>""",
"satzfunk-player": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-labelledby="title desc"><title id="title">SatzfunkPlayer — the composed image and playback</title><desc id="desc">An editorial frame carries a visible poster and a playback timeline</desc><rect width="256" height="256" rx="48" fill="#eceee7"/><g stroke="#283733" fill="none" stroke-linejoin="round"><rect x="47" y="73" width="162" height="116" rx="10" stroke-width="8"/><path d="M47 160h162" stroke-width="6"/><path d="M69 142l34-37 28 24 26-37 34 50" stroke-width="7"/><path d="M70 177h115" stroke-width="6" stroke-linecap="round"/></g><circle cx="114" cy="177" r="7" fill="#a07755"/><circle cx="171" cy="92" r="7" fill="#a07755"/></svg>"""
}
STYLE = """
/* Semantic Instruments: three evidenced families, not an empty capability matrix. */
.catalog-index .catalog-heading.semantic-heading {padding-bottom:2.4rem}
.semantic-heading .eyebrow {font-size:.69rem; letter-spacing:.19em}
.catalog-index .semantic-heading h1 {font-size:clamp(3.6rem,9vw,6.8rem);letter-spacing:-.075em;max-width:18ch;margin:14px 0 24px}
.semantic-heading .lead {max-width:45rem;color:var(--ink);font-size:clamp(1.12rem,2.5vw,1.48rem);line-height:1.52}
.semantic-heading .sublead {max-width:48rem;color:var(--muted);font-size:.98rem;margin:1.25rem 0 0;line-height:1.55}
.semantic-grid {grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(14px,2vw,30px)}
.semantic-grid .instrument-tile {display:block;color:var(--ink);transition:transform .16s ease;text-decoration:none}
.semantic-grid .instrument-tile:hover {transform:translateY(-2px)}
.semantic-grid .instrument-icon {border-radius:22.37%;padding:0;overflow:hidden;aspect-ratio:1;background:#eceee7;border:1px solid var(--line)}
.semantic-grid .instrument-icon img {display:block;width:100%;height:100%;object-fit:cover}
.semantic-grid .instrument-tile:hover .instrument-icon,.semantic-grid .instrument-tile:focus-visible .instrument-icon{border-color:var(--ink);background:#eceee7}
.semantic-grid .instrument-name {font-size:clamp(1.35rem,2.5vw,2rem);font-weight:650;line-height:1.18;margin:18px 0 8px;letter-spacing:-.04em}
.semantic-grid .instrument-meta {font:600 .70rem/1.3 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--muted);letter-spacing:.045em;text-transform:uppercase;margin-bottom:10px}
.semantic-grid .instrument-description {display:block;font-size:.95rem;line-height:1.48;color:var(--muted)}
.semantic-grid .instrument-tile:focus-visible {outline:2px solid var(--accent);outline-offset:7px;border-radius:9px}
.semantic-sequence {display:flex;align-items:center;gap:1rem;margin-top:2rem;padding-top:1.25rem;border-top:1px solid var(--line);font-size:.86rem;letter-spacing:.015em;color:var(--muted);flex-wrap:wrap}
.semantic-sequence strong {color:var(--ink);font-weight:650}
.semantic-sequence .arrow {color:#a07755;font-size:1.2rem}
.semantic-details {display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:clamp(12px,3vw,36px);margin:0;padding:25px 0;border-top:1px solid var(--line)}
.semantic-details h3 {font-size:1.3rem;letter-spacing:-.035em}
.semantic-details p {margin:0 0 10px;max-width:47ch;color:var(--muted)}
.semantic-details .semantic-state {font-size:.76rem;line-height:1.5;color:var(--muted)}
.semantic-details .semantic-state strong {color:var(--ink)}
.semantic-details a {font-size:.85rem}
.reference-links {display:flex;gap:1rem 1.65rem;flex-wrap:wrap;padding:0;list-style:none}
.reference-links li {font-size:.89rem}
.semantic-standards {font-size:.92rem;line-height:1.65;max-width:52rem;color:var(--muted)}
@media(max-width:720px) {
 .semantic-grid {grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
 .semantic-grid .instrument-name {font-size:1.08rem;margin:10px 0 4px}
 .semantic-grid .instrument-description {font-size:.80rem}
 .semantic-grid .instrument-meta {font-size:.58rem}
 .semantic-details {grid-template-columns:1fr;gap:.5rem}
}
@media(max-width:480px) {
 .semantic-grid {grid-template-columns:repeat(2,minmax(0,1fr))}
 .semantic-grid li:last-child {grid-column:1 / 2}
 .semantic-heading .lead {font-size:1.14rem}
}
@media(prefers-reduced-motion:reduce) {.semantic-grid .instrument-tile {transition:none}}
"""
def main_markup(prefix):
    asset=lambda name: prefix+"assets/"+name
    home=prefix or "/"
    return '''<main id="main" class="catalog-index">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="https://fountain.coach/">Fountain Coach</a></li><li aria-current="page">Instruments</li></ol></nav>
    <header class="catalog-heading semantic-heading">
      <div class="eyebrow">Fountain Coach · executable artistic capabilities</div>
      <h1>Instruments</h1>
      <p class="lead">Instruments make, hear and present artistic work. They have independent implementations, observable behaviour, and a place in a composition.</p>
      <p class="sublead">The instrument is not its library, its transport or its historical framework. What matters is what it can do, how it can participate, and what has actually been demonstrated.</p>
    </header>
    <section class="instrument-index" aria-labelledby="featured-title">
      <div class="section-heading"><div><div class="eyebrow">The active instrument field</div><h2 id="featured-title">Three distinct acts.</h2></div><p>These are developing software capabilities at different acceptance stages—not three already certified MIDI 2.0 instruments.</p></div>
      <ul class="instrument-grid semantic-grid" aria-label="Sing, Ear and SatzfunkPlayer">
       <li><a class="instrument-tile" href="#sing"><span class="instrument-icon"><img src="''' + asset('instrument-sing.svg') + '''" alt="Sing symbol: vocal source and radiating resonance" width="256" height="256"></span><span class="instrument-name">Sing</span><span class="instrument-meta">01 · synthesis</span><span class="instrument-description">A voice becomes an instrument: phonemes, notes, pressure and time produce sound.</span></a></li>
       <li><a class="instrument-tile" href="#ear"><span class="instrument-icon"><img src="''' + asset('instrument-ear.svg') + '''" alt="Ear symbol: arriving arcs converge at a listening point" width="256" height="256"></span><span class="instrument-name">Ear</span><span class="instrument-meta">02 · listening</span><span class="instrument-description">Sound is heard and measured, rather than treated as a file that merely exists.</span></a></li>
       <li><a class="instrument-tile" href="#satzfunk-player"><span class="instrument-icon"><img src="''' + asset('instrument-satzfunk-player.svg') + '''" alt="SatzfunkPlayer symbol: composed frame with image and timeline" width="256" height="256"></span><span class="instrument-name">SatzfunkPlayer</span><span class="instrument-meta">03 · presentation</span><span class="instrument-description">A recording becomes a listenable edition with an intentional poster image.</span></a></li>
      </ul>
      <div class="semantic-sequence" aria-label="Artistic relation"><strong>Voice</strong><span class="arrow" aria-hidden="true">→</span><strong>Listening</strong><span class="arrow" aria-hidden="true">→</span><strong>Published hearing</strong></div>
    </section>
    <section class="rule" aria-labelledby="evidence-title"><div class="eyebrow">Present implementation</div><h2 id="evidence-title">What is actually running?</h2>
      <article id="sing" class="semantic-details"><div><h3>Sing · a voice</h3><p>An original, native singing synthesizer whose phonetic states are played through typed MIDI 2.0 events. The persistent audio renderer has produced PCM and a macOS output witness.</p><a href="https://github.com/Fountain-Coach/sing">Source and current evidence ↗</a></div><div class="semantic-state"><strong>Development instrument.</strong> Native synthesis and typed-note rehearsal verified. Perceived intelligibility, full real-time performance and physical MIDI reception remain to be accepted.</div></article>
      <article id="ear" class="semantic-details"><div><h3>Ear · a listening boundary</h3><p>An AudioWorklet observation of sound, with measured levels and connections to a browser-local MIDI 2.0 event plane. It can participate in an instrument's feedback, without masquerading as an arbitrary microphone.</p><a href="https://github.com/Fountain-Coach/Reframe/blob/main/docs/evidence/r12-csound-ear-midi2-v10-20261014.md">Worklet witness and limits ↗</a></div><div class="semantic-state"><strong>Research and integration.</strong> Real browser observations demonstrated; a separately admitted physical instrument and iPad Safari acceptance are not yet established.</div></article>
      <article id="satzfunk-player" class="semantic-details"><div><h3>SatzfunkPlayer · a published-image decision</h3><p>A reusable listening player with Semantic Poster Imaging: select and compose a legible, source-bound image for the player, catalogue and social sharing. The poster is editorial work, not a random decoded frame.</p><a href="https://satzfunk.fountain.coach/">Hear the published Satzfunk archive ↗</a></div><div class="semantic-state"><strong>Software instrument candidate.</strong> Independent source and eight tests exist. Automated frame extraction, semantic vision and poster publication are still to be implemented; not yet an admitted MIDI 2.0 instrument.</div></article>
    </section>
    <section class="rule" aria-labelledby="foundations-title"><div class="eyebrow">Previous catalogue · retained reference</div><h2 id="foundations-title">Foundational capabilities</h2><p class="semantic-standards">The earlier catalogue is preserved as technical and historical evidence. It no longer defines the three featured instruments; its components may still be used by present work.</p>
      <ul class="reference-links"><li><a href="https://instruments.fountain.coach/instruments/codex-auth-instrument/">Codex Login Instrument ↗</a></li><li><a href="https://instruments.fountain.coach/instruments/semantic-browser/">Semantic Browser ↗</a></li><li><a href="https://instruments.fountain.coach/instruments/csound-auv3/">Csound AUv3 ↗</a></li></ul>
    </section>
    <section class="rule" aria-labelledby="status-title"><div class="eyebrow">Operating context</div><h2 id="status-title">What makes an instrument?</h2><p class="semantic-standards">An instrument has a declared purpose, bounded inputs and outputs, a responsible source owner, and evidence of its behavior. A MIDI 2.0 instrument must additionally meet its governed profile, lifecycle and transport obligations. Instruments is a supporting capability catalogue; <a href="https://midi2.fountain.coach/">MIDI2</a> documents the shared operational plane, <a href="https://teatro.fountain.coach/">Teatro</a> composes, and <a href="https://satzfunk.fountain.coach/">Satzfunk</a> publishes admitted hearings.</p></section>
    </main>'''.replace('href="#','href="#')
def rewrite(page, prefix):
    s=page.read_text()
    matches=list(re.finditer(r'<main\b[^>]*\bid="main"[^>]*>.*?</main>',s,flags=re.S|re.I))
    assert len(matches)==1,(str(page),len(matches))
    s=s[:matches[0].start()]+main_markup(prefix)+s[matches[0].end():]
    s=s.replace('Fountain Coach MIDI2 Instruments','Fountain Coach Instruments')
    s=s.replace('The published Fountain Coach association-dependent MIDI2 instrument catalogue for the Reframe ecosystem.',
                'Sing, Ear and SatzfunkPlayer: making, listening and presenting in the Fountain Coach instrument field.')
    s=s.replace('A growing index of Fountain Coach MIDI2 instruments for the Reframe ecosystem.',
                'Sing, Ear and SatzfunkPlayer: three evolving artistic software capabilities.')
    s=s.replace('Fountain Coach MIDI2 catalogue grid with one admitted Codex Login Instrument and open instrument fields',
                'Fountain Coach Instruments editorial triad: Sing, Ear and SatzfunkPlayer')
    s=s.replace('association-dependent MIDI2 instrument', 'artistic software instrument')
    if prefix == '/instruments/':
        assert 'fc-shell-reel' in s and 'data-estate-identity="instruments"' in s
    page.write_text(s)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--prefix',choices=['/','/instruments/'],required=True)
    ap.add_argument('--asset-origin',type=Path,default=None)
    a=ap.parse_args()
    page=a.root/'index.html';css=a.root/'assets/site.css'
    assert page.exists() and css.exists()
    if a.asset_origin:
        for slug in LOGOS:shutil.copy2(a.asset_origin/f'instrument-{slug}.svg',a.root/'assets'/f'instrument-{slug}.svg')
    else:
        for slug,data in LOGOS.items(): (a.root/'assets'/f'instrument-{slug}.svg').write_text(data+'\n')
    assert 'Semantic Instruments: three evidenced families' not in css.read_text()
    with css.open('a') as f:f.write('\n'+STYLE)
    rewrite(page,a.prefix)
    print('SEMANTIC_PAGE_UPDATED',page)
if __name__=='__main__':main()
