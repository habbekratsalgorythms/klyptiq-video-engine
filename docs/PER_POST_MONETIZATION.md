# Klyptiq — monetisatie en auteursrechten per post (besluit 8 november 2026)

**Doel:** commerciële, eigen gamingcontent combineren met echte niet-gemonetiseerde journalistieke/fananalyses over populaire games, zonder blind te vertrouwen op een platformschakelaar. Iedere publicatie is een **nieuw**, apart en aan de exacte montage gekoppeld rechtenrecord. De vier-post-per-dag-doelstelling mag nooit een blokkade omzeilen.

## De drie categorieën

| Code | Content | Behandeling |
| --- | --- | --- |
| `owned_commercial` | Originele hardwaretests, eigen AI-personages, eigen illustraties en video's waarvan alle commerciële rechten vaststaan | Advertenties/sponsors/affiliate alleen waar de toepasselijke rechten en platformtoelating voor de exacte video zijn aangetoond. Eerst menselijke kwaliteit-/rechtenvrijgave. |
| `unpaid_game_analysis` | Nieuws, kritiek of echte fragmentgerichte bespreking van grote games, zonder inkomsten op deze post | Rechtmatig bronmateriaal, citaatrecht (Auteurswet 15a), uitgeversvoorwaarden, aanvullende rechten, commerciële context van het merk en de daadwerkelijke platforminstellingen per post beoordelen. Bij quote: menselijke juridische beoordeling; **geen auto-post**. |
| `owned_unpaid` | Originele gratis communityposts, polls en infographics zonder derdepartijassets | Wel feitelijk en rechtenmatig verifiëren. Het uitzetten van opbrengsten is geen garantie dat de platforms geen advertenties tonen. |

## Wel en niet te regelen per platform

- **YouTube gewone video's:** via YouTube Studio > Content > video > Monetization > Off > Save, mits de betreffende monetisatiebediening beschikbaar is. Documenteer bij de exacte video de daadwerkelijke status. YouTube kan zelf of namens een rechthebbende advertenties tonen, ook als Klyptiq niet verdient. Off is **geen** auteursrechtlicentie.
- **YouTube Shorts:** Shorts-advertentie-inkomsten lopen via de Shorts Monetization Module (deels kanaalbreed). Een betrouwbare universele uitknop per afzonderlijke Short is niet bevestigd. Behandel het dus niet alsof een onafhankelijke instelling altijd beschikbaar is; vraag platform/accountcontrole en gebruik bij twijfel uitsluitend eigen content.
- **TikTok:** verschillende betaalprogramma's hebben verschillende voorwaarden. Het afzonderlijk uitschrijven van een gamevideo uit een specifiek Gaming Incentive Program is niet hetzelfde als Creator Rewards of universeel inkomsten uitschakelen. Controleer het daadwerkelijke account; neem niet aan dat Metricool deze instellingen kan wijzigen.
- **Instagram:** Gifts, branded content en eventuele andere inkomstenprogramma's verschillen. Geen universeel betrouwbaar 'monetization off' per Instagram Post/Reel bevestigd. Geen automatische aanname vanuit onze planner.
- **Metricool connector:** ondersteunt sociale publicatie, niet het schakelen van platformadvertentie-inkomsten per post. `autoPublish:false` betekent push-notificatie in plaats van API-autopublicatie; `draft:true` bewaart als concept. **Geen van beide velden is een monetisatie-instelling.**

Officiële bronnen:
- https://support.google.com/youtube/answer/6332943
- https://support.google.com/youtube/answer/12504220
- https://support.google.com/youtube/answer/2475463
- https://ads.tiktok.com/resources/help/article/how-to-troubleshoot-unsuccessful-updates-to-organization-account?lang=nl-NL
- https://support.rockstargames.com/articles/7bNaeoMFTV0iUDGhStTXvz/policy-on-posting-copyrighted-rockstar-games-material
- https://wetten.overheid.nl/jci1.3:c:BWBR0001886&artikel=15a

## Specifiek voor Rockstar-fanmateriaal

Rockstar's publiek beleid biedt beperkte ruimte voor incidenteel **niet-commercieel** fanmateriaal door individuele fans. In dezelfde tekst staat dat het beleid niet bedoeld is voor commerciële film/TV/online exploitatie, advertenties en digitale uitgevers. Een kanaal met sponsor-/affiliateaanbiedingen kan niet automatisch aannemen dat `monetization:none` de promo-doelstelling uitwist. Groei van volgers voor een commercieel merk telt mee bij de juridische context. Voor uitroepen van 'vrij door citaatrecht' moet het exact gebruikte fragment onmisbaar zijn voor concrete kritiek of beoordeling, proportioneel en voorzien van bronvermelding; in deze twijfelgevallen geldt menselijk juridisch oordeel, geen AI-publicatieknop.

Dit blokkeert niet het publiceren van **eigen originele berichten over een game** zonder beschermde beelden, muziek of gameplay: de feiten moeten gecontroleerd zijn en merkgebruik mag geen verwarring scheppen, maar er wordt dan geen auteursrechtelijk beschermd spelbeeld hergebruikt.

## Werkwijze: wat doet onze engine?

Per post, voor publicatie:
1. Maak een `publication_rights_preflight.py`-record met de exacte hash van de definitieve video (geen nieuw render zonder nieuwe toets), feitencontrole, lijst van alle assets en citaat/vergunning per fragment.
2. Zet `publication_category`, `monetization` en één object in `platform_posts` per platform met het werkelijke formaat, concrete inkomsteninstelling en bewijs van handmatige controle.
3. Vul `brand_growth_intent`, `affiliate_links`, `paid_partner`, `product_or_service_cta` en `paid_boost` eerlijk in. Een affiliate-link op een als 'niet betaald' aangemerkte post veroorzaakt **BLOCK**.
4. Draai lokaal `python3 scripts/per_post_revenue_preflight.py /private/path/per-post-record.json`. Een fout/beslissing die menselijke juridische beoordeling vereist geeft exitcode 2.
5. Publiceer pas na de aparte menselijke rechtencontrole, account/platformcontrole en finale expliciete toestemming voor de exacte video. Deze tool wijzigt zelf geen platforms of geplande posts.

De resultaten zijn:
- `BLOCK`: onvoldoende of tegenstrijdige gegevens / onveilig monetisatieregime.
- `MANUAL_LEGAL_REVIEW_REQUIRED`: de claim steunt op citaatrecht of derdepartij-gamebeelden; volledige menselijke juridische beoordeling nodig.
- `READY_FOR_OWNER_AND_PLATFORM_REVIEW`: alleen eigen commerciële of eigen niet-betaalde media, alle documentatie present; geen definitieve publicatietoestemming.

**Bestaande Metricool-planning:** de vorige controle had 14 eerdere GTA VI-posts als drafts gezet (`autoPublish:false`); deze wijziging activeert die posts niet en zet geen betaalprogramma's aan. Verifieer status opnieuw voordat iets wordt vrijgegeven. Een concept is geen gepubliceerd of gemonetiseerd bericht.

## Test
`python3 -m unittest discover -s tests -p test_per_post_revenue.py -v`

**Grenzen:** dit is softwarematig beleid, geen juridisch bindend advies, geen platform-API-capaciteit en geen mogelijkheid om TikTok/Instagram/YouTube-verdiensten daadwerkelijk te wijzigen. Een juridische uitzondering kan contextafhankelijk ook in commerciële redactionele content gelden; we veronderstellen noch dat dit altijd mag, noch dat commerciële context op zichzelf altijd betekent dat artikel 15a onmogelijk is.
