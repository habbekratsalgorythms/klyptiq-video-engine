# Klyptiq — verplichte citaatrechttoets vóór iedere publicatie

**Besluit eigenaar (8 november 2026):** controleer bij ieder nieuw bericht of iedere video het Nederlandse citaatrecht, als er beelden/geluiden van derden worden gebruikt. Onderbouw per publicatie én per fragment en bekijk het in relatie tot de eigen inhoudelijke kritiek of beoordeling. Dit is een verplicht werkproces, geen permanente toestemming voor fragmenten.

## Bronnen (opnieuw verifiëren bij veranderend recht)
- Auteurswet artikel 15a: https://wetten.overheid.nl/jci1.3:c:BWBR0001886&artikel=15a
- Wet op de naburige rechten, artikel 10(b): https://wetten.overheid.nl/BWBR0005921/2025-07-01/0/Hoofdstuk7
- NVJ juristen over audiovisuele citaten: https://nvj.nl/diensten/juridische-ondersteuning/mag-dat-zomaar
- Rockstar actuele rechtenpolicy: https://support.rockstargames.com/articles/7bNaeoMFTV0iUDGhStTXvz/policy-on-posting-copyrighted-rockstar-games-material
- YouTube gamevideo-beleid: https://support.google.com/youtube/answer/138161
- YouTube monetization/reused-content-beleid: https://support.google.com/youtube/answer/1311392

## De zeven vragen die je echt moet beantwoorden

1. **Rechtmatig openbaar gemaakt?** Het fragment komt uit een legitiem publiek toegankelijk bronwerk; geen leaks, geen onrechtmatig gekopieerd pre-release materiaal.
2. **Aantoonbaar citaatdoel?** Beschrijft, beoordeelt, bekritiseert of analyseert de eigen vertelling het fragment zelf? Licht precies toe welke visuele eigenschap wordt bekritiseerd of verklaard.
3. **Functionele relatie?** Heeft de kijker het exact geciteerde fragment nodig om de eigen analyse te begrijpen, of is het uitsluitend sfeervol opvulmateriaal? Sfeer/background alleen => geen citaatrechtbasis.
4. **Proportionaliteit?** Zijn aantal en exacte lengte van de geciteerde onderdelen noodzakelijk voor dat doel? Geen magisch aantal seconden. Lange trailercompilatie + generieke voice-over is verdacht.
5. **Persoonlijkheids- en naburige rechten?** Geen verminking/misleidende montage, rekening houden met de maker en audiovisuele producent/uitvoerende kunstenaars.
6. **Bronvermelding?** De oorspronkelijke bron en maker zo duidelijk als redelijkerwijs mogelijk in beeld en/of beschrijving.
7. **Commerciële bestemming en platform?** Controleer advertenties, affiliate-links, gesponsorde posts, productpromotie en YouTube/TikTok/IG-regels apart. Citaatrecht kan ook in een commercieel werk spelen, maar dat is een contextafhankelijke wettelijke uitzondering, géén automatische toestemming van de rechthebbende of garantie op platformmonetisatie.

## Dagelijkse uitvoering — niet te omzeilen

- Bij **elk** nieuw bericht: herkomst van alle gebruikte media, feiten en licenties vaststellen. Eigen originele tekst/beelden mogen automatisch gepland worden na aantoonbare rechten-/feitcheck volgens de bestaande Klyptiq-agentinstructies.
- Bij derdepartijfragmenten: maak een specifiek rechtenrecord voor juist deze versie van de montage (SHA256 van MP4/bijbehorende edit), publicatieplatform, verdienmodel en iedere uitgeknipte seconde.
- Documenteer het citaatdoel, de concrete eigen kritiek, waarom juist deze clip, waarom deze lengte, bronvermelding en uitgevers-/naburige rechten. Vraag een menselijke inhoudelijke/juridische toets van de **exacte** video en commerciële context. Een AI-agent geeft niet zelfstandig definitieve juridische toestemming.
- Voor **screenshot- en fotoposts** geldt dezelfde doelgerichte toets. Zet in het record `asset_type: image` en motiveer `why_this_image_is_necessary` en `why_image_extent_is_proportionate`; bevestig `generic_poll_or_decoration: false` alleen als de afbeelding werkelijk onderwerp van specifieke kritiek of beoordeling is. Een generieke vraag aan volgers met een promotionele officiële screenshot kwalificeert niet automatisch. Ook een goed gedocumenteerde afbeelding blijft `HUMAN_LEGAL_DECISION_REQUIRED`.
- Zonder de verplichte bewijzen: **BLOCK**. Als alles gedocumenteerd lijkt maar het citaatrecht de enige rechtsbasis is: **HUMAN_LEGAL_DECISION_REQUIRED**. Laat dit nooit automatisch op social platforms plaatsen.
- Bij uitsluitend eigen of commercieel passend gelicentieerde assets kan de geautomatiseerde documentatie **READY_FOR_FINAL_HUMAN_REVIEW** rapporteren; ook dat is geen publicatietoestemming.
- Gebruik `python3 scripts/publication_rights_preflight.py /secure/private/path/video-review.json --output /secure/private/path/video-rights-result.json`. Een niet-gereed record eindigt met exitcode 2. Werk niet met klantgegevens of licentiedocumenten in de openbare repository.
- De Metricool-autopublicatietaak is aangepast zodat de vier-postsnorm **nooit** geldt als vrijbrief voor onbeoordeelde beelden. Niet goedgekeurd betekent niet plaatsen, ook wanneer daardoor minder berichten live komen.
- Controleer al eerder ingeplande posts eveneens vóór het live gaan voor zover de aangesloten interface wijzigingen mogelijk maakt. Deze workflow houdt zelf geen directe blokkade van al externe Metricool-geplande taken in: daarvoor moet de Metricool-koppeling of publicatie-engine daadwerkelijk een rechtencheck afdwingen.

## De huidige GTA VI-V3/V4-voorbeelden
- V3 en V4 zijn reviews uit officieel Rockstar-materiaal met rechten voor commerciële exploitatie **niet vastgesteld**.
- De videos bevatten deels montage van officiële clips als visuele basis en korte generieke voice-over. Er is geen gedocumenteerd fragment-voor-fragment oordeel over de proportionaliteit als citaat.
- Daarom blijven commerciële publicatie en inkomsten via deze edits **geblokkeerd**. Een technisch succesvolle FFmpeg-render of bronvermelding wijzigt dat niet.
- Als een toekomstige video een specifiek shot inhoudelijk bespreekt, kan een advocaat/jurist met de exacte montage, bron en context beoordelen of artikel 15a van toepassing is. Dat is geen algemeen akkoord voor Rockstar-videocompilaties.

**Opmerking:** deze checks verkleinen risico's, maar een programma kan de uiteindelijke juridische beoordeling of het oordeel van een platform/rechter niet vervangen.
