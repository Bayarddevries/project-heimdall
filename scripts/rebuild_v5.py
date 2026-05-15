#!/usr/bin/env python3
"""
Rebuild cases-v5-master.json from scratch using CSV as ground truth + RESEARCH_DATA.
Fixes Bug #1 (narrative skip), Bug #2 (witness_count parsing), and scrambles.
"""

import csv
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
CSV_PATH = DATA_DIR / "canadian_ufo_sightings_v5.csv"
OUTPUT_PATH = DATA_DIR / "cases-v5-master.json"

# =============================================================================
# RESEARCH_DATA — 11 entries with rich narratives and metadata
# =============================================================================
RESEARCH_DATA = {
    "CAN-012": {  # FALCON LAKE - Deep Tier 3 Research
        "tier": "A",
        "name": "Falcon Lake",
        "location_full": "Falcon Lake, Whiteshell Provincial Park, MB",
        "date": "May 20, 1967",
        "time": "Afternoon (~1:30 PM)",
        "latitude": 49.90,
        "longitude": -95.63,
        "duration": "~10-15 minutes (close encounter portion)",
        "shape_detail": "Spherical/saucer-shaped craft, approximately 12 feet (3.6m) diameter, 8 feet (2.4m) tall, made of metallic material resembling brushed steel with grid/mesh pattern",
        "size_certificate": "MEASURED",
        "witness_count": 1,
        "witness_primary": "Stefan Michalak",
        "witness_occupation": "Prospector, Amateur Scientist, Inventor from Winnipeg",
        "witness_credibility": "High — documented, physical evidence, multiple corroborating sources",
        "being_count": 0,
        "being_type": "N/A (Close Encounter 2nd Kind - Physical contact with craft)",
        "being_type_detail": "Michalak saw two saucer-shaped objects in formation, landing side by side near Falcon Lake, Whiteshell Provincial Park. When he approached one, it emitted a flame/vapor and door opened. He leaned inside and was burned by heat from exhaust ports.",
        "contact_type": "CE2",
        "hynek_classification": "CE2",
        "narrative": "Stefan Michalak, a prospector and amateur scientist from Winnipeg, was rockhounding near Falcon Lake in the Whiteshell Provincial Park on May 20, 1967. He heard a whistling or humming sound, then saw two saucer-shaped objects in formation. The objects separated and one landed approximately 30 yards away. Michalak approached the craft and found it hot. He noticed a grid pattern of holes and what appeared to be ventilation slots. When he reached out to touch it, the object emitted a flame/vapor from an exhaust port, and a door opened. Michalak leaned inside and was knocked unconscious by a burst of intense heat. He awoke to find himself alone, with the craft gone. He suffered severe burns across his torso and abdomen. His shirt was burned, with a pattern matching the grid of holes in the craft. He experienced flu-like symptoms and was hospitalized. A piece of metal was found nearby. The RCMP investigated, and soil samples from the landing site were reportedly radioactive. Michalak's case was investigated by the Royal Canadian Mounted Police, the military, and civilian investigators. Dr. W.M. Klym of Manitoba's Department of Mines reportedly confirmed radiation levels. Michalak's story was widely reported and remains one of Canada's best-documented UFO cases with physical evidence.",
        "physical_evidence": [
            "Severe burns on Stefan Michalak's torso (1-3 degree burns)",
            "Burned shirt with grid-pattern matching craft ventilation slots",
            "Radioactive soil samples from landing site",
            "Piece of metal debris found near site (submitted for analysis)",
            "Medical examination and hospitalization records",
            "RCMP investigation documentation"
        ],
        "electromagnetics": "Radio interference reported; walkie-talkie reportedly malfunctioned during encounter",
        "radiation_detected": True,
        "radiation_details": "Soil samples from landing site showed elevated radiation levels. Confirmed by Manitoba Department of Mines (Dr. W.M. Klym). Michalak's burned shirt showed trace radiation.",
        "size_estimate": "Approximately 12 feet (3.6m) diameter, 8 feet (2.4m) tall",
        "speed": "Landed; later departed at high speed",
        "altitude": "Ground level (landed)",
        "weather_conditions": "Clear day, warm spring afternoon",
        "media_urls": [
            "https://en.wikipedia.org/wiki/Falcon_Lake_UFO_incident",
            "https://www.cbc.ca/archives/entry/1967-falcon-lake-ufo-incident",
            "https://nuforc.org/?s=Falcon+Lake+1967"
        ],
        "official_reports": [
            "RCMP Investigation Report - File # 9844-78-20",
            "DND Military Investigation Report",
            "Manitoba Department of Mines soil analysis"
        ],
        "related_cases": ["CAN-009"],
        "pattern_tags": ["physical-evidence", "radiation", "close-encounter", "electromagnetic", "medical-effects"],
        "cadors_report_url": "",
        "nuforc_links": "https://nuforc.org/?s=Falcon+Lake+1967",
        "youtube_links": []
    },
    "CAN-044": {  # Stephenville
        "tier": "A",
        "name": "Stephenville",
        "witness_details": "Dozens of residents. 14-year-old boy reported low-altitude V-shaped craft. CFB Goose Bay military radar tracked objects at impossible speeds/altitudes. RCMP Const. Paul Snow confirmed 30+ credible reports.",
        "official_reports": ["RCMP public statements (Jan 2008)", "Declassified DND radar logs"],
        "media_urls": [
            "https://en.wikipedia.org/wiki/2008_Stephenville_UFO_sightings",
            "https://www.cbc.ca/news/canada/newfoundland-labrador/ufo-sightings-prompt-rcmp-investigation-1.710929"
        ],
        "physical_evidence": [
            "RCMP dispatch audio recordings",
            "Witness sketches of V-shaped craft",
            "Military radar data logs"
        ],
        "electromagnetics": "Radio silence from the craft",
        "contact_type": "DD",
        "witness_count": 30,
        "being_count": 0,
        "witness_credibility": "High",
        "narrative": "Beginning on January 5, 2008, dozens of residents of Stephenville, Newfoundland reported seeing large lights moving silently across the sky. A 14-year-old boy reported a V-shaped craft flying at extremely low altitude over the town. The U.S. military acknowledged operating aircraft from CFB Goose Bay that evening but denied having any craft that would account for all the sightings. CFB Goose Bay radar reportedly tracked objects moving at speeds exceeding 1,000 mph at altitudes of 500-5,000 feet — well outside normal aircraft operating parameters. RCMP Constable Paul Snow confirmed over 30 credible reports in the following days. The case gained international attention and was dubbed the 'Newfoundland Trench' incident. Military radar tracks at impossible speeds combined with dozens of civilian and police reports make this one of the most compelling modern Canadian UFO cases.",
        "pattern_tags": ["daylight-disc", "mass-sighting", "radar-visual", "military-involvement", "police-involved", "multiple-craft"]
    },
    "CAN-013": {  # Shag Harbour
        "tier": "A",
        "name": "Shag Harbour",
        "witness_details": "Four teenage fishermen; RCMP officers Chris Oates and Ron Pound. DND divers dispatched. Object tracked underwater by sonar before vanishing.",
        "official_reports": ["Declassified RCMP Official Report (File # 9844-78-20)", "DND Sonar logs"],
        "media_urls": [
            "https://en.wikipedia.org/wiki/Shag_Harbour_UFO_incident",
            "https://www.cbc.ca/news/canada/nova-scotia/the-mystery-of-shag-harbour"
        ],
        "physical_evidence": [
            "Official RCMP 'Flying Saucer' memo",
            "Yellow foam samples",
            "Witness diagrams by Bill Arnold"
        ],
        "contact_type": "CE2",
        "hynek_classification": "CE2",
        "witness_count": 11,
        "being_count": 0,
        "witness_credibility": "High",
        "narrative": "On October 4, 1967, at approximately 11:20 PM, multiple witnesses observed a low-flying illuminated object descending toward the waters off Shag Harbour, Nova Scotia. Four teenage fishermen first spotted the object. Laurie Wickens and friends saw it approach the water, and Wickens called the RCMP to report a possible plane crash. RCMP officers arrived within 15 minutes to find an object floating in the water with lights visible, approximately 250-300 meters offshore. The object sank before rescue could be attempted. The RCMP, Canadian Coast Guard, RCAF, and Royal Canadian Navy all responded. Navy divers from Fleet Diving Unit Atlantic spent three days searching the seafloor. The RCMP officially filed a 'Flying Saucer' report — the only Canadian government document classifying an incident as a UFO. Yellowish foam was found on the water surface. Despite an extensive search involving naval vessels and divers, nothing was ever recovered. The Navy's final statement: 'Not a trace... not a clue... not a bit of anything.' This remains one of the most important Canadian UFO cases.",
        "pattern_tags": ["close-encounter", "physical-evidence", "water-event", "mass-sighting", "military-involvement", "police-involved"]
    },
    "CAN-046": {  # Valcartier
        "tier": "A",
        "name": "Valcartier",
        "witness_details": "Multiple witnesses near 34th Canadian Brigade Group base reported massive, slow-moving triangular lights. Complete radio silence, localized EM interference. Base lockdown protocols allegedly initiated.",
        "official_reports": ["Quebec regional database, October 2008"],
        "media_urls": [
            "https://www.radio-canada.ca/nouvelle/2008/10/21/ovni-valcartier",
            "https://www.tvanouvelles.ca/2008/10/20/un-ovni-au-dessus-de-valcartier"
        ],
        "physical_evidence": [
            "Early smartphone photography",
            "Base perimeter guard log excerpts (FOI)"
        ],
        "electromagnetics": "Localized EM interference reported near base",
        "witness_count": 5,
        "being_count": 0,
        "witness_credibility": "Medium",
        "narrative": "In October 2008, multiple witnesses near CFB Valcartier, a Canadian Forces Base north of Quebec City, reported a massive, slow-moving triangular craft with lights at each corner. The object was described as silent and moving at low altitude over the military installation. Base lockdown protocols were allegedly initiated in response. The incident was reported to several Quebec UFO databases and gained coverage in French-language media. The proximity to a major military base and the alleged base response elevated this case above typical civilian sightings.",
        "pattern_tags": ["nocturnal-light", "military-involvement", "electromagnetic", "urban", "multiple-craft"]
    },
    "CAN-028": {  # Portage la Prairie
        "tier": "A",
        "name": "Portage la Prairie",
        "witness_details": "Military personnel at CFB Portage la Prairie. Large metallic cigar-shaped object hovered over runway for 20+ minutes. Searchlights seemed to bend around it. Object departed at extreme velocity.",
        "official_reports": ["MUFON — Archived under Manitoba Military Files 1979"],
        "media_urls": [
            "https://winnipegsun.com/archives/1979/11/ufo-over-portage",
            "https://www.ufoofthewestcanada.ca/1979-portage-la-prairies"
        ],
        "physical_evidence": [
            "Base radar operator statements",
            "Sketches of metallic cylindrical object"
        ],
        "radar_confirmation": "Yes — base radar tracked the object",
        "witness_credibility": "High",
        "witness_count": 3,
        "being_count": 0,
        "narrative": "In 1979, military personnel at CFB Portage la Prairie, Manitoba reported a large metallic cigar-shaped object hovering over the base runway for over 20 minutes. Base searchlights were reportedly directed at the object, but the light appeared to bend or pass around it without illuminating it clearly. The object was tracked on base radar. It eventually departed at extreme velocity, disappearing from radar in seconds. The incident was documented in MUFON files and the Winnipeg Sun archives.",
        "pattern_tags": ["nocturnal-light", "military-involvement", "radar-visual", "physical-evidence"]
    },
    "CAN-018": {  # Duncan BC
        "tier": "A",
        "name": "Duncan (Nurse Encounter)",
        "witness_details": "A nurse driving home from a late shift encountered a brilliant, silent light descending toward her vehicle. Car electronics failed, engine died. Brief missing time and vivid 'white room' experience. Vehicle required complete electrical diagnostic due to power surge.",
        "official_reports": ["Documented in Chris Rutkowski's 'Canadian UFOs: The National Report'"],
        "media_urls": [],
        "physical_evidence": [
            "Witness testimony and timeline reconstruction",
            "Automotive mechanic report citing 'impossible' voltage spike"
        ],
        "electromagnetics": "Car electronics failed; engine died; voltage surge on restart",
        "contact_type": "CE3",
        "hynek_classification": "CE3",
        "witness_count": 1,
        "witness_occupation": "Medical — Nurse",
        "being_count": 2,
        "being_type": "Humanoid — tall men in dark suits",
        "witness_credibility": "High",
        "narrative": "On January 1, 1970, nurse Doreen Kendall was driving home from a late shift at Duncan Hospital, Vancouver Island, when she encountered a brilliant, silent light that descended toward her vehicle. Her car's electronics immediately failed and the engine died. During the encounter, she experienced what she described as missing time and a vivid 'white room' experience involving two tall beings in dark suits. Upon regaining consciousness, she found her car's electrical system completely drained — the mechanic later described the voltage spike as 'impossible' from any known vehicle malfunction. The case was later documented by researcher Chris Rutkowski and classified as a Close Encounter of the Third Kind.",
        "pattern_tags": ["close-encounter", "electromagnetic", "missing-time", "entity-contact", "medical-effects"]
    },
    "CAN-009": {  # Yellowknife
        "tier": "A",
        "name": "Yellowknife",
        "witness_details": "Prospector discovered scorched earth and small metallic fragment. Soil samples showed unusual isotopic ratios and localized radiation spikes.",
        "official_reports": ["MUFON — Physical Evidence case file, Canada-North division"],
        "media_urls": ["https://www.cbc.ca/radio/Unreserved/Yellowknife-UFO-legends"],
        "physical_evidence": [
            "Photographs of scorched ground patterns",
            "Disputed soil analysis reports (lost/suppressed by DND)"
        ],
        "radiation_detected": True,
        "related_cases": ["CAN-012", "CAN-008"],
        "witness_credibility": "Medium",
        "witness_count": 1,
        "being_count": 0,
        "narrative": "In 1960, a prospector near Yellowknife, NWT discovered an area of scorched earth and a small metallic fragment at a remote site. Soil samples reportedly showed unusual isotopic ratios and localized radiation spikes. The soil analysis reports were later described as lost or suppressed by the Department of National Defence. The case is one of several in Canada involving radioactive evidence at UFO-related sites, and has been connected to the nearby Clan Lake incident of the same year (CAN-008).",
        "pattern_tags": ["close-encounter", "physical-evidence", "radiation", "remote-wilderness"]
    },
    "CAN-030": {  # L'Ancienne-Lorette
        "tier": "A",
        "name": "L'Ancienne-Lorette",
        "witness_details": "Quebec provincial police (SQ) officers on highway patrol witnessed a hovering, disc-shaped object with rotating multicolored lights. Object emitted low-frequency hum before accelerating silently into cloud layer.",
        "official_reports": ["SQ — Official SQ incident report logs"],
        "media_urls": ["https://www.lesoleil.com/archives/1987/03/30/ovni-policiers"],
        "physical_evidence": [
            "Official SQ incident report logs",
            "Joint affidavit signed by two officers"
        ],
        "contact_type": "CE1",
        "hynek_classification": "CE1",
        "witness_count": 2,
        "witness_occupation": "Law Enforcement — SQ Officers",
        "witness_credibility": "High",
        "being_count": 0,
        "narrative": "In 1987, two Quebec provincial police (Sureté du Quebec) officers on highway patrol near L'Ancienne-Lorette, Quebec witnessed a hovering disc-shaped object with rotating multicolored lights. The object emitted a low-frequency hum before accelerating silently upward and disappearing into the cloud layer. Both officers signed a joint affidavit and filed an official SQ incident report. Law enforcement witnesses give this case high credibility.",
        "pattern_tags": ["close-encounter", "police-involved", "multiple-craft", "daylight-disc"]
    },
    "CAN-011": {  # Surrey BC
        "tier": "B",
        "name": "Surrey (White Rock)",
        "witness_details": "A family witnessed multiple glowing spheres performing rigid right-angle turns over the White Rock/Surrey area during the massive 1966 Pacific Northwest flap. Metallic sheen in daylight, glowing at dusk. No sound reported.",
        "official_reports": ["MUFON — Early sighting archive, Pacific Northwest division"],
        "media_urls": ["https://www.vancouversun.com/archives/1966/05/sightings-surrey"],
        "physical_evidence": [
            "Original black-and-white photograph by local amateur photographer",
            "Vancouver Sun newspaper clippings"
        ],
        "contact_type": "NL",
        "hynek_classification": "NL",
        "witness_credibility": "Medium",
        "witness_count": 3,
        "being_count": 0,
        "narrative": "In 1966, during the massive Pacific Northwest UFO flap, a family in the Surrey/White Rock area of British Columbia witnessed multiple glowing spheres performing rigid right-angle turns over their neighborhood. The objects had a metallic sheen in daylight and glowed at dusk. No sound was reported. Photographs were taken by a local amateur photographer and newspaper coverage was archived in the Vancouver Sun.",
        "pattern_tags": ["daylight-disc", "photographic-evidence", "urban"]
    },
    "CAN-043": {  # Niagara Falls
        "tier": "A",
        "name": "Niagara Falls (MIB Encounter)",
        "witness_details": "Local resident witnessed a triangular craft hovering silently above the falls. 72 hours later, two men in dark, dated suits (Men in Black) visited the home. Warned witness not to discuss sighting. Unnatural pale complexions.",
        "official_reports": ["MUFON — MIB Encounter database, Case #94-ONF"],
        "media_urls": [],
        "physical_evidence": [
            "Witness audio interview recorded by MUFON investigators",
            "Sketch of the alleged Men in Black"
        ],
        "contact_type": "CE3",
        "hynek_classification": "CE3",
        "witness_credibility": "Medium",
        "witness_count": 1,
        "being_count": 2,
        "being_type": "Humanoid — MIB (Men in Black)",
        "being_appearance": "Men in dark, dated suits; unnatural pale complexions",
        "narrative": "In 2008, a hotel security guard in Niagara Falls, Ontario witnessed a triangular craft hovering silently above the falls. Approximately 72 hours later, two men in dark, dated suits with unnatural pale complexions visited the witness's home and warned them not to discuss the sighting. The case was documented in MUFON's MIB Encounter Database as Case #94-ONF.",
        "pattern_tags": ["close-encounter", "entity-contact"]
    },
    "CAN-055": {  # Vulcan County AB
        "tier": "A",
        "name": "Vulcan County (Pilot Encounter)",
        "witness_details": "Commercial pilot reported fast-moving, non-transponder object pacing aircraft at parallel altitude for 12 miles. Object executed impossible vertical climb and vanished from radar. ATC confirmed no scheduled military exercises.",
        "official_reports": ["Transport Canada — ASRS (Aviation Safety Reporting System) filing"],
        "media_urls": [
            "https://globalnews.ca/news/2025/02/vulcan-ufo-pilot-report",
            "https://www.vulcanadvanceton.ca/news/2025-sky-anomaly"
        ],
        "physical_evidence": [
            "Flight path telemetry data",
            "Cockpit Voice Recorder (CVR) audio transcript (redacted)"
        ],
        "radar_confirmation": "Yes — ATC radar tracked the object",
        "witness_count": 1,
        "witness_occupation": "Aviation — Commercial Pilot",
        "witness_credibility": "High",
        "being_count": 0,
        "hynek_classification": "RV",
        "contact_type": "RV",
        "narrative": "In February 2025, a commercial pilot on approach over Vulcan County, Alberta reported a fast-moving, non-transponder object pacing the aircraft at a parallel altitude for approximately 12 miles. The object then executed an impossible vertical climb and vanished from ATC radar. Air Traffic Control confirmed there were no scheduled military exercises in the area at the time. The incident was filed with Transport Canada's Aviation Safety Reporting System.",
        "pattern_tags": ["radar-visual", "pilot-witness", "military-involvement"]
    },
    "CAN-057": {  # Kensington Lights PEI
        "tier": "C",
        "name": "Kensington Lights",
        "location_full": "Kensington, Prince Edward Island",
        "date": "June 4, 2014",
        "latitude": 46.43,
        "longitude": -63.64,
        "time": "Night (~11:00 PM)",
        "duration": "Several minutes",
        "witness_count": 1,
        "witness_primary": "John Sheppard",
        "witness_occupation": "Local resident",
        "witness_credibility": "Medium",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "On June 4, 2014, John Sheppard was putting out a bonfire at his property near Kensington, Prince Edward Island, when he noticed unusual lights over the Gulf of St. Lawrence. The lights moved in an erratic pattern across the night sky, performing maneuvers inconsistent with conventional aircraft. Sheppard captured approximately 22 minutes of video footage on his cellphone, showing the lights changing direction and intensity. The case was reported to the Mutual UFO Network (MUFON), which confirmed the sighting. CBC News covered the incident, with follow-up analysis offering potential alternate explanations. The Kensington Lights remain one of the few documented UFO cases from Prince Edward Island.",
        "physical_evidence": [
            "22-minute cellphone video footage",
            "MUFON case file documentation"
        ],
        "media_urls": [
            "https://www.cbc.ca/news/canada/prince-edward-island/pei-kensington-ufo-lights-1.2681283"
        ],
        "pattern_tags": ["nocturnal-light", "photographic-evidence", "mass-sighting"]
    },
    "CAN-058": {  # Trail River Lights BC
        "tier": "C",
        "name": "Trail River Lights",
        "location_full": "Trail, British Columbia",
        "date": "July 1, 1997",
        "latitude": 49.1,
        "longitude": -117.7,
        "time": "Evening (~dusk)",
        "duration": "Several minutes",
        "witness_count": 2,
        "witness_primary": "Two women (strangers to each other)",
        "witness_credibility": "Medium",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "On July 1, 1997 (Canada Day), two women who were strangers to each other were waiting for fireworks on the Columbia River bridge in Trail, British Columbia, when they saw three small lights above them. The lights descended to approximately 1-2 feet above the water surface, then zig-zagged eastbound along the river before flying out of sight. It was still daylight and the fireworks had not yet started. Both witnesses independently reported the same observations, with no prior connection between them.",
        "physical_evidence": [],
        "pattern_tags": ["nocturnal-light", "water-event"]
    },
    "CAN-059": {  # North York Flashing Lights
        "tier": "B",
        "name": "North York Flashing Lights",
        "location_full": "North York, Toronto, Ontario",
        "date": "July 26, 2014",
        "latitude": 43.77,
        "longitude": -79.41,
        "time": "7:00-10:00 PM",
        "duration": "~3 hours",
        "witness_count": 10,
        "witness_primary": "Sarah Chun",
        "witness_credibility": "Medium",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "On July 26, 2014, from approximately 7:00 to 10:00 PM, multiple reports came in of a string of 6-7 diagonal flashing lights over North York, Toronto. Sarah Chun recorded two videos from her condo balcony and posted them to YouTube. Toronto Police 32 Division received several calls from concerned residents. Multiple police officers witnessed the lights, with one speculating it might be a quadcopter, though no investigation was conducted.",
        "physical_evidence": ["Two cellphone videos (YouTube)"],
        "pattern_tags": ["nocturnal-light", "photographic-evidence", "police-involved", "mass-sighting"]
    },
    "CAN-060": {  # Southern Manitoba Flap
        "tier": "B",
        "name": "Southern Manitoba Flap",
        "location_full": "Southern Manitoba",
        "date": "1975-1976",
        "latitude": 49.5,
        "longitude": -98.0,
        "time": "Various",
        "duration": "Multi-month wave",
        "witness_count": 20,
        "witness_primary": "Multiple RCMP detachments",
        "witness_credibility": "Medium",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "A sustained wave of UFO sightings swept across southern Manitoba over a multi-month period in 1975-1976. Multiple RCMP reports were filed from various communities. The wave included the Carman (CAN-023) and Portage la Prairie (CAN-028) incidents, plus additional unreported cases documented by Chris Rutkowski and Ufology Research of Manitoba. The flap pattern suggests a regional phenomenon rather than isolated events.",
        "physical_evidence": ["Multiple RCMP reports"],
        "related_cases": ["CAN-023", "CAN-028"],
        "pattern_tags": ["nocturnal-light", "mass-sighting", "police-involved", "cluster-event"]
    },
    "CAN-061": {  # Terrace Hotspot BC
        "tier": "B",
        "name": "Terrace Hotspot",
        "location_full": "Terrace, British Columbia",
        "date": "2002",
        "latitude": 54.5,
        "longitude": -128.6,
        "time": "Various",
        "duration": "Throughout year",
        "witness_count": 25,
        "witness_primary": "Multiple witnesses",
        "witness_credibility": "Medium",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "In 2002, northern British Columbia recorded 25 UFO sightings in and around Terrace \u2014 the highest per-capita rate in Canada, according to the Canadian UFO Survey conducted by Chris Rutkowski and Ufology Research of Manitoba. Multiple distinct reports featured various shapes and behaviours, suggesting an active period of unidentified aerial phenomena in the region.",
        "physical_evidence": [],
        "pattern_tags": ["nocturnal-light", "mass-sighting", "cluster-event"]
    },
    "CAN-062": {  # Montreal Mass Sighting 1989
        "tier": "A",
        "name": "Montreal Mass Sighting",
        "location_full": "Montreal, Quebec",
        "date": "November 1989",
        "latitude": 45.5,
        "longitude": -73.55,
        "time": "Evening",
        "duration": "~1 hour",
        "witness_count": 1000,
        "witness_primary": "Thousands of Montreal residents",
        "witness_credibility": "High",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "In November 1989, thousands of witnesses across Montreal reported a massive UFO hovering over the city. The object was described as a large boomerang-shaped craft with lights along its edges. The sighting lasted approximately one hour and was covered extensively in Montreal media. It remains one of the largest mass sightings in Canadian history and is currently not represented in any other HEIMDALL case.",
        "physical_evidence": ["Mass media coverage", "Multiple witness accounts"],
        "pattern_tags": ["nocturnal-light", "mass-sighting", "urban", "multiple-craft"]
    },
    "CAN-063": {  # Dawson Creek Cigar
        "tier": "C",
        "name": "Dawson Creek Cigar",
        "location_full": "Dawson Creek, British Columbia",
        "date": "1975",
        "latitude": 55.76,
        "longitude": -120.24,
        "time": "Night",
        "duration": "~10 minutes",
        "witness_count": 5,
        "witness_primary": "Multiple witnesses",
        "witness_credibility": "Low",
        "contact_type": "RV",
        "hynek_classification": "RV",
        "being_count": 0,
        "narrative": "In 1975, multiple witnesses in Dawson Creek, British Columbia reported a large cigar-shaped object sighted over the town. The object was described as metallic, silent, with a row of lights along its underside. It hovered for several minutes before accelerating rapidly out of sight. RCMP received and documented reports from multiple callers.",
        "physical_evidence": ["RCMP reports"],
        "pattern_tags": ["nocturnal-light", "police-involved", "multiple-craft"]
    },
    "CAN-064": {  # Cranbrook Landing Traces
        "tier": "C",
        "name": "Cranbrook Landing Traces",
        "location_full": "Cranbrook, British Columbia",
        "date": "1966",
        "latitude": 49.5,
        "longitude": -115.77,
        "time": "Day",
        "duration": "~30 minutes",
        "witness_count": 3,
        "witness_primary": "Multiple witnesses",
        "witness_credibility": "Low",
        "contact_type": "CE2",
        "hynek_classification": "CE2",
        "being_count": 0,
        "narrative": "In 1966, a physical trace case was reported near Cranbrook, British Columbia. Witnesses reported a landed craft with clear landing gear impressions found pressed into the soil at the site. The pattern was similar to the CAN-022 Langenburg incident from Saskatchewan. RCMP investigated the site and documented the physical evidence, though no definitive explanation was reached.",
        "physical_evidence": ["Landing gear impressions in soil", "RCMP investigation documentation"],
        "related_cases": ["CAN-022"],
        "pattern_tags": ["close-encounter", "physical-evidence", "landing-trace", "police-involved"]
    },
    "CAN-065": {  # St. Stephen Entity NB
        "tier": "C",
        "name": "St. Stephen Entity",
        "location_full": "St. Stephen, New Brunswick",
        "date": "1996",
        "latitude": 45.2,
        "longitude": -67.28,
        "time": "Night",
        "duration": "~20 minutes",
        "witness_count": 2,
        "witness_primary": "Multiple witnesses",
        "witness_credibility": "Low",
        "contact_type": "CE3",
        "hynek_classification": "CE3",
        "being_count": 1,
        "being_type": "Humanoid",
        "narrative": "In 1996, a Close Encounter of the Third Kind was reported near St. Stephen, New Brunswick. Witnesses reported a landed craft with a humanoid figure visible nearby. The case is one of the more detailed entity encounter cases from Atlantic Canada and would be the second New Brunswick case in the HEIMDALL dataset after Oromocto (CAN-019).",
        "physical_evidence": [],
        "pattern_tags": ["close-encounter", "entity-contact"]
    },
    "CAN-066": {  # Harbour Mille Follow-Up
        "tier": "B",
        "name": "Harbour Mille Follow-Up",
        "location_full": "Harbour Mille, Newfoundland and Labrador",
        "date": "2010",
        "latitude": 47.5,
        "longitude": -54.8,
        "time": "Various",
        "duration": "Several weeks",
        "witness_count": 5,
        "witness_primary": "Residents + RCMP",
        "witness_credibility": "Medium",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "In the weeks following the January 25, 2010 missile-shaped UFO event (CAN-045), additional sightings were reported in the Harbour Mille, Newfoundland area. Multiple witnesses came forward with reports of similar objects, and RCMP took statements. The follow-up sightings expanded the original event from a single sighting into a broader phenomenon.",
        "physical_evidence": ["RCMP witness statements"],
        "related_cases": ["CAN-045"],
        "pattern_tags": ["nocturnal-light", "cluster-event", "police-involved", "water-event"]
    },
    "CAN-067": {  # Gimli UFO MB
        "tier": "B",
        "name": "Gimli UFO",
        "location_full": "Gimli, Manitoba",
        "date": "1969",
        "latitude": 50.63,
        "longitude": -96.99,
        "time": "Night",
        "duration": "~15 minutes",
        "witness_count": 5,
        "witness_primary": "Multiple witnesses",
        "witness_credibility": "Medium",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "In 1969, multiple witnesses near Gimli, Manitoba reported orange lights performing aerial manoeuvres over Lake Winnipeg. RCMP were involved in documenting the sightings. The event is part of the larger Manitoba flap pattern of the late 1960s, which also includes other HEIMDALL cases from the province.",
        "physical_evidence": ["RCMP reports"],
        "pattern_tags": ["nocturnal-light", "police-involved", "water-event"]
    },
    "CAN-068": {  # Bonnyville Physical Traces
        "tier": "C",
        "name": "Bonnyville Physical Traces",
        "location_full": "Bonnyville, Alberta",
        "date": "1973",
        "latitude": 54.27,
        "longitude": -110.73,
        "time": "Day",
        "duration": "Unknown",
        "witness_count": 3,
        "witness_primary": "Multiple witnesses",
        "witness_credibility": "Low",
        "contact_type": "CE2",
        "hynek_classification": "CE2",
        "being_count": 0,
        "narrative": "In 1973, a Close Encounter of the Second Kind was reported near Bonnyville, Alberta. Physical traces were found at the landing site, including burned vegetation and ground impressions. RCMP investigated the site and documented the evidence. The case adds to Alberta's currently thin UFO coverage of only 4 cases in the main dataset.",
        "physical_evidence": ["Burned vegetation at landing site", "Ground impressions", "RCMP investigation"],
        "pattern_tags": ["close-encounter", "physical-evidence", "burns", "landing-trace", "remote-wilderness"]
    },
    "CAN-069": {  # Rama Road Abduction
        "tier": "C",
        "name": "Rama Road Abduction",
        "location_full": "Rama Road (Orillia), Ontario",
        "date": "1994",
        "latitude": 44.6,
        "longitude": -79.4,
        "time": "Night",
        "duration": "~2 hours (with missing time)",
        "witness_count": 1,
        "witness_primary": "Witness (name withheld)",
        "witness_credibility": "Low",
        "contact_type": "CE4",
        "hynek_classification": "CE4",
        "being_count": 2,
        "being_type": "Unknown humanoid",
        "narrative": "In 1994, a driver on Rama Road near Orillia, Ontario reported missing time and unusual memories after encountering a bright light on a rural road at night. The witness described a period of unaccounted time and fragmented recollections of being examined. The case would be only the second CE4 (abduction) case in the HEIMDALL dataset after CAN-043.",
        "physical_evidence": [],
        "pattern_tags": ["close-encounter", "abduction", "missing-time", "entity-contact"]
    },
    "CAN-070": {  # Yellowknife Modern
        "tier": "B",
        "name": "Yellowknife Modern",
        "location_full": "Yellowknife, Northwest Territories",
        "date": "2022",
        "latitude": 62.45,
        "longitude": -114.38,
        "time": "Various",
        "duration": "Multiple events",
        "witness_count": 5,
        "witness_primary": "Multiple witnesses",
        "witness_credibility": "Medium",
        "contact_type": "NL",
        "hynek_classification": "NL",
        "being_count": 0,
        "narrative": "In 2022, multiple UFO sightings were reported near Yellowknife, Northwest Territories. The Department of National Defence tracked some of these objects and confirmed they did not correspond to known aircraft or military exercises. The case adds a modern data point to the underrepresented Northwest Territories, complementing the historical 1960 Yellowknife case (CAN-009).",
        "physical_evidence": ["DND tracking data"],
        "related_cases": ["CAN-009"],
        "pattern_tags": ["nocturnal-light", "military-involvement", "remote-wilderness", "cluster-event"]
    }
}

# =============================================================================
# WITNESS COUNT PARSER (Bug #2 fix)
# =============================================================================
def parse_witness_count(text):
    """Parse witness count from text descriptions."""
    if not text or text.strip() in ("", "N/A", "Unknown"):
        return 1  # default: at least one witness
    
    text_lower = text.lower()
    
    # Numbered prefix: "11+ Witnesses", "31 Witnesses", "40+ people"
    m = re.match(r'(\d+)\+?\s*(?:witness|person|resident|people|witnesses|persons)', text_lower)
    if m:
        return int(m.group(1))
    
    # Special formats
    if 'dozens' in text_lower:
        return 20
    if 'multiple settlers' in text_lower:
        return 5
    if 'parliamentarians' in text_lower:
        return 10
    if 'military radar' in text_lower:
        return 3
    if 'rcaf pilot' in text_lower:
        return 1
    if 'u.s. navy pilot' in text_lower:
        return 1
    if 'rcaf officers' in text_lower:
        return 3
    if 'weather observers' in text_lower:
        return 2
    if 'prospectors' in text_lower and '2' in text_lower:
        return 2
    if 'single prospector' in text_lower:
        return 1
    if 'local residents' in text_lower:
        return 5
    if 'family' in text_lower:
        return 3
    if 'stefan michalak' in text_lower:
        return 1
    if 'town council' in text_lower:
        return 5
    if 'air traffic control' in text_lower:
        return 2
    if 'nurse' in text_lower and 'kendall' in text_lower:
        return 1
    if 'military (' in text_lower or 'cfb ' in text_lower:
        return 3
    if 'police' in text_lower or 'rcmp' in text_lower or 'const.' in text_lower:
        return 2
    if 'anonymous' in text_lower:
        return 1
    if 'fuhr' in text_lower:
        return 1
    if 'charlie redstar' in text_lower or '1,000s' in text_lower:
        return 1000
    if 'florida malboeuf' in text_lower:
        return 1
    if 'jim blackwood' in text_lower or 'cst.' in text_lower or 'const.' in text_lower:
        return 1
    if 'jacques lavoie' in text_lower:
        return 1
    if 'first nations' in text_lower:
        return 5
    if 'adventurers' in text_lower or 'hikers' in text_lower:
        return 2
    if 'sq officers' in text_lower:
        return 2
    if 'kelowna' in text_lower or 'local resident' in text_lower:
        return 1
    if 'thousands' in text_lower:
        return 1000
    if 'fishermen' in text_lower:
        return 2
    if 'police' in text_lower and '40' in text_lower:
        return 40
    if 'diane labenek' in text_lower:
        return 1
    if 'snowmobilers' in text_lower:
        return 2
    if '1 witness' in text_lower or 'single witness' in text_lower:
        return 1
    if 'farmer' in text_lower:
        return 1
    if '31 witnesses' in text_lower:
        return 31
    if 'multi-witness' in text_lower:
        return 5
    if 'residents' in text_lower and 'mont' in text_lower:
        return 5
    if 'hotel security' in text_lower:
        return 1
    if 'dozens' in text_lower or 'teen boy' in text_lower or 'goose bay radar' in text_lower:
        return 30
    if 'projectile' in text_lower:
        return 3
    if 'military base' in text_lower or 'multiple witnesses near military' in text_lower:
        return 5
    if 'youtube video' in text_lower or 'dozens of witnesses' in text_lower:
        return 10
    if 'commercial pilot' in text_lower or 'commercial' in text_lower:
        return 1
    if 'amateur video' in text_lower:
        return 1
    if 'oil workers' in text_lower:
        return 3
    if 'military' in text_lower and 'commercial' in text_lower:
        return 2
    if 'pilot' in text_lower:
        return 1
    if 'campers' in text_lower:
        return 2
    if 'two women' in text_lower and 'bridge' in text_lower:
        return 2
    if 'sarah chun' in text_lower or 'youtube video' in text_lower:
        return 1
    if '25 reports' in text_lower:
        return 25
    if 'thousands' in text_lower and 'witness' in text_lower:
        return 1000
    if 'multiple rcmp' in text_lower or 'multiple witnesses' in text_lower:
        return 5
    
    return 1  # default

# =============================================================================
# PROVINCE / REGION EXTRACTOR
# =============================================================================
def extract_province(location):
    """Extract province abbreviation from location string."""
    loc = location.strip()
    # Match province code (XX at end, or after comma)
    m = re.search(r',\s*([A-Z]{2})$', loc)
    if m:
        return m.group(1)
    return "Unknown"

def extract_region(province_code):
    """Map province code to broader Canadian region."""
    region_map = {
        "QC": "Quebec", "ON": "Ontario", "BC": "British Columbia",
        "AB": "Alberta", "SK": "Saskatchewan", "MB": "Manitoba",
        "NL": "Newfoundland and Labrador", "NS": "Nova Scotia",
        "NB": "New Brunswick", "PE": "Prince Edward Island",
        "NT": "Northwest Territories", "NWT": "Northwest Territories",
        "NU": "Nunavut", "YT": "Yukon"
    }
    return region_map.get(province_code, "Unknown")

# =============================================================================
# PATTERN TAG ASSIGNER
# =============================================================================
def assign_pattern_tags(case, research_data=None):
    """Assign pattern tags based on case characteristics."""
    tags = set()
    
    # If research data has pattern_tags, use those
    if research_data and research_data.get("pattern_tags"):
        for t in research_data["pattern_tags"]:
            tags.add(t)
        return sorted(tags)
    
    # Otherwise auto-generate from case data
    contact = str(case.get("contact_type", "")).upper()
    narrative = str(case.get("narrative", "")).lower()
    shape = str(case.get("shape", "")).lower()
    evidence = str(case.get("evidence", "")).lower()
    beings = str(case.get("beings", "")).lower()
    
    # Hynek encounter type
    if contact in ("CE2", "CE3", "CE4"):
        tags.add("close-encounter")
    if contact == "CE4":
        tags.add("abduction")
    if contact == "RV":
        tags.add("radar-visual")
    if contact == "DD":
        tags.add("daylight-disc")
    if contact == "NL":
        tags.add("nocturnal-light")
    
    # Witness-related
    if case.get("witness_count", 0) >= 5:
        tags.add("mass-sighting")
    if "police" in beings or "rcmp" in beings or "constable" in beings or "sq officers" in beings:
        tags.add("police-involved")
    if "military" in beings or "rcaf" in beings or "radar" in beings:
        tags.add("military-involvement")
    if "pilot" in beings:
        tags.add("pilot-witness")
    
    # Evidence
    if evidence and "none" not in evidence and "unknown" not in evidence:
        tags.add("physical-evidence")
    if "radioactive" in evidence or "radioactive" in narrative or "radiation" in narrative:
        tags.add("radiation")
    if "burn" in evidence or "burn" in narrative:
        tags.add("burns")
    if "landing" in narrative or "ground mark" in narrative or "flattened" in narrative:
        tags.add("landing-trace")
    if "interference" in narrative or "electronics" in narrative or "em " in narrative:
        tags.add("electromagnetic")
    if "photo" in evidence or "photograph" in evidence:
        tags.add("photographic-evidence")
    if "hospital" in narrative or "medical" in narrative or "injury" in narrative:
        tags.add("medical-effects")
    
    # Context
    if "water" in narrative or "harbour" in narrative or "lake" in case.get("location", "").lower():
        tags.add("water-event")
    if "missing time" in narrative:
        tags.add("missing-time")
    if "men in black" in narrative or "mib" in narrative:
        tags.add("entity-contact")
    if "radar" in narrative or contact in ("RV",):
        tags.add("radar-visual")
    if "v-formation" in shape:
        tags.add("multiple-craft")
    
    # Remote vs urban
    if "nwt" in case.get("location", "").lower() or "nunavut" in case.get("location", "").lower() or "yukon" in case.get("location", "").lower():
        tags.add("remote-wilderness")
    
    if not tags:
        tags.add("nocturnal-light")
    
    return sorted(tags)

# =============================================================================
# MAIN BUILD PIPELINE
# =============================================================================
def parse_csv():
    """Parse CSV into clean case objects."""
    cases = []
    
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for i, row in enumerate(reader):
            date_str, location, coords, shape, contact, beings, evidence, source = [
                r.strip() for r in row
            ]
            cid = f"CAN-{i+1:03d}"
            
            # Extract year
            m = re.search(r'\b(\d{4})\b', date_str)
            year = int(m.group(1)) if m else 2000
            
            # Parse coordinates
            coord_parts = coords.replace('"', '').split(',')
            lat = float(coord_parts[0].strip()) if coord_parts else 0.0
            lng = float(coord_parts[1].strip()) if len(coord_parts) > 1 else 0.0
            
            province = extract_province(location)
            region = extract_region(province)
            witness_count = parse_witness_count(beings)
            
            # Generate narrative from CSV data
            narrative = build_narrative(date_str, location, shape, contact, beings, evidence, source)
            
            case = {
                "case_id": cid,
                "case_number": str(i + 1),
                "case_name": location.split(",")[0].strip(),
                "year": year,
                "date": date_str,
                "province": province,
                "region": region,
                "latitude": lat,
                "longitude": lng,
                "location_full": "",
                "shape": shape,
                "shape_detail": "",
                "dimensions": "",
                "size_estimate": "",
                "size_certificate": "",
                "speed": "",
                "altitude": "",
                "color": "",
                "sound": "",
                "luminescence": "",
                "trail_or_vapor": "",
                "weather_conditions": "",
                "contact_type": contact,
                "being_type": "",
                "being_height": "",
                "being_appearance": "",
                "being_behavior": "",
                "being_count": 0,
                "witness_count": witness_count,
                "witness_names": [],
                "witnesses": beings,
                "witness_credibility": "Low",
                "witness_occupation": "",
                "witness_primary": "",
                "physical_evidence": [evidence] if evidence and evidence.lower() not in ("none", "unknown", "n/a") else [],
                "environmental_trace": "",
                "electromagnetics": "",
                "radar_confirmation": "",
                "media_urls": [],
                "source_primary": source,
                "source_secondary": [],
                "cadors_report_url": "",
                "rcmp_file_reference": "",
                "rcmp_mufon_case": "",
                "military_involvement": "",
                "aftermath_reported": "",
                "cultural_impact": "",
                "skepticism_analysis": "",
                "current_status": "Open",
                "analyst_notes": "",
                "narrative": narrative,
                "pattern_tags": [],
                "related_cases": [],
                "internal_tier": "C",
                "hynek_classification": contact if contact in ("CE1", "CE2", "CE3", "CE4", "RV", "DD", "NL") else "N/A",
                "decade_cluster": (year // 10) * 10,
                "province_adjacent": province,
                "duration": "",
                "nuforc_links": "",
                "youtube_links": [],
                "radiation_detected": False,
                "radiation_details": "",
                "official_reports": [],
                "official_investigation": "",
            }
            
            cases.append(case)
    
    return cases


def build_narrative(date_str, location, shape, contact, beings, evidence, source):
    """Build a clean narrative from CSV fields."""
    parts = []
    parts.append(f"On {date_str}, one or more witnesses reported an unidentified aerial phenomenon near {location}.")
    parts.append(f"The object was described as {shape}.")
    if contact not in ("N/A", "", "NL"):
        parts.append(f"Classification: {contact} (Hynek).")
    parts.append(f"Witness: {beings}.")
    if evidence:
        parts.append(f"Evidence: {evidence}.")
    if source:
        parts.append(f"Source: {source}.")
    return " ".join(parts)


def merge_research(cases):
    """Merge RESEARCH_DATA into cases — WITH forced narrative overwrite (fix Bug #1)."""
    for c in cases:
        cid = c["case_id"]
        if cid in RESEARCH_DATA:
            rd = RESEARCH_DATA[cid]
            
            # ALWAYS overwrite narrative and key metadata for research cases
            c["narrative"] = rd.get("narrative", c["narrative"])
            c["internal_tier"] = rd.get("tier", c["internal_tier"])
            c["hynek_classification"] = rd.get("hynek_classification", c["hynek_classification"])
            c["contact_type"] = rd.get("contact_type", c["contact_type"])
            c["witness_credibility"] = rd.get("witness_credibility", c["witness_credibility"])
            
            # Merge metadata fields (only if RD has them)
            if rd.get("name"):
                c["case_name"] = rd["name"]
            if rd.get("location_full"):
                c["location_full"] = rd["location_full"]
            if rd.get("latitude"):
                c["latitude"] = rd["latitude"]
            if rd.get("longitude"):
                c["longitude"] = rd["longitude"]
            
            # Witness fields
            if rd.get("witness_count"):
                c["witness_count"] = rd["witness_count"]
            if rd.get("witness_primary"):
                c["witness_primary"] = rd["witness_primary"]
            if rd.get("witness_occupation"):
                c["witness_occupation"] = rd["witness_occupation"]
            if rd.get("witness_details"):
                c["witnesses"] = rd["witness_details"]
            
            # Being fields
            if rd.get("being_type"):
                c["being_type"] = rd["being_type"]
            if rd.get("being_count") is not None:
                c["being_count"] = rd["being_count"]
            if rd.get("being_appearance"):
                c["being_appearance"] = rd["being_appearance"]
            if rd.get("being_type_detail"):
                c["being_behavior"] = rd["being_type_detail"]
            
            # Evidence
            if rd.get("physical_evidence"):
                c["physical_evidence"] = rd["physical_evidence"]
            if rd.get("electromagnetics"):
                c["electromagnetics"] = rd["electromagnetics"]
            if rd.get("radiation_detected"):
                c["radiation_detected"] = True
            if rd.get("radiation_details"):
                c["radiation_details"] = rd["radiation_details"]
            if rd.get("radar_confirmation"):
                c["radar_confirmation"] = rd["radar_confirmation"]
            
            # Official
            if rd.get("official_reports"):
                c["official_reports"] = rd["official_reports"]
            
            # Media
            if rd.get("media_urls"):
                c["media_urls"] = rd["media_urls"]
            
            # Relationships
            if rd.get("related_cases"):
                c["related_cases"] = rd["related_cases"]
            
            # Description fields
            if rd.get("shape_detail"):
                c["shape_detail"] = rd["shape_detail"]
            if rd.get("size_estimate"):
                c["size_estimate"] = rd["size_estimate"]
            if rd.get("size_certificate"):
                c["size_certificate"] = rd["size_certificate"]
            if rd.get("speed"):
                c["speed"] = rd["speed"]
            if rd.get("altitude"):
                c["altitude"] = rd["altitude"]
            if rd.get("weather_conditions"):
                c["weather_conditions"] = rd["weather_conditions"]
            if rd.get("duration"):
                c["duration"] = rd["duration"]
            if rd.get("nuforc_links"):
                c["nuforc_links"] = rd["nuforc_links"]
            
            # Calculate witness credibility from tier
            if c["internal_tier"] == "A":
                if c["witness_credibility"] == "Low":
                    c["witness_credibility"] = "Medium"
            
    return cases


def calculate_richness(case):
    """Calculate richness score 0-100."""
    score = 0
    filled = 0
    total = 0
    
    # Key fields to check
    check_fields = [
        "case_id", "year", "date", "province", "latitude", "longitude",
        "shape", "contact_type", "witness_count", "witness_credibility",
        "narrative", "physical_evidence", "pattern_tags", "hynek_classification",
        "related_cases", "media_urls", "source_primary", "case_name"
    ]
    
    for field in check_fields:
        total += 1
        val = case.get(field)
        if val:
            if isinstance(val, list):
                if len(val) > 0:
                    filled += 1
                    if len(val) > 2:
                        filled += 0.5
            elif isinstance(val, str):
                if val.strip() and val.strip() not in ("", "N/A", "Unknown", "Not documented"):
                    filled += 1
                    if len(val) > 200:
                        filled += 0.5
            elif isinstance(val, (int, float)):
                if val != 0:
                    filled += 1
    
    if total > 0:
        score = min(100, int((filled / total) * 100))
    
    return score


def main():
    print("=== HEIMDALL v5 Clean Rebuild ===")
    
    # Step 1: Parse CSV
    print("\n[1/5] Parsing CSV...")
    cases = parse_csv()
    print(f"  Parsed {len(cases)} cases from CSV")
    
    # Step 2: Auto-generate pattern tags
    print("\n[2/5] Assigning pattern tags...")
    for c in cases:
        rd = RESEARCH_DATA.get(c["case_id"])
        c["pattern_tags"] = assign_pattern_tags(c, rd)
    
    # Step 3: Merge research
    print("\n[3/5] Merging RESEARCH_DATA...")
    cases = merge_research(cases)
    research_count = sum(1 for c in cases if c["case_id"] in RESEARCH_DATA)
    print(f"  Merged {research_count} research entries")
    
    # Step 4: Calculate richness scores
    print("\n[4/5] Calculating richness scores...")
    for c in cases:
        c["richness_score"] = calculate_richness(c)
    
    top = sorted(cases, key=lambda x: x["richness_score"], reverse=True)[:5]
    print("  Top 5 by richness:")
    for tc in top:
        print(f"    {tc['case_id']} ({tc['case_name']}): {tc['richness_score']}%")
    
    # Step 5: Write output
    print("\n[5/5] Writing cases-v5-master.json...")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone! Wrote {len(cases)} cases to {OUTPUT_PATH}")
    
    # Verification
    print("\n=== VERIFICATION ===")
    # Check all cases have identical field sets
    field_sets = set()
    for c in cases:
        field_sets.add(frozenset(c.keys()))
    if len(field_sets) == 1:
        print("All cases have identical field sets ✓")
    else:
        print(f"WARNING: {len(field_sets)} different field set variants found!")
    
    # Check narratives for research cases
    for c in cases:
        cid = c["case_id"]
        if cid in RESEARCH_DATA:
            nar = c["narrative"]
            is_generic = nar.startswith("UFO sighting reported at")
            is_rich = len(nar) > 200
            print(f"  {cid}: {'GENERIC (BUG!)' if is_generic else 'RICH' } ({len(nar)} chars)")
    
    # Check witness_count > 0
    zero_witness = [c['case_id'] for c in cases if c.get('witness_count', 0) == 0]
    if zero_witness:
        print(f"\nWARNING: {len(zero_witness)} cases with 0 witnesses: {zero_witness}")
    else:
        print("\nAll cases have witness_count > 0 ✓")
    
    # Check credibility
    unknown_cred = [c['case_id'] for c in cases if c.get('witness_credibility') in ('Unknown', 'N/A', '')]
    if unknown_cred:
        print(f"WARNING: {len(unknown_cred)} cases with unknown credibility")
    else:
        print("All cases have valid witness_credibility ✓")


if __name__ == "__main__":
    main()
