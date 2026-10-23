/* Shared data for Workshop 4 (slides.html and workbook.html).
   Every finding below is paraphrased from the paper's abstract (retrieved via Europe PMC / Crossref, Oct 2026).
   "n" is given only when the abstract states it ("n/r" = not reported in the abstract).
   This is a curated reading list, NOT a systematic review: empty cells in the evidence map mean
   "no study in this list", not "no study exists". */
window.WS4 = (function () {
  var MODALITIES = [
    { id: "smell",  label: "Smell" },
    { id: "music",  label: "Music / sound" },
    { id: "food",   label: "Taste / food" },
    { id: "visual", label: "Vision / images" },
    { id: "temp",   label: "Temperature / touch" },
    { id: "multi",  label: "Multisensory / VR" }
  ];
  var OUTCOMES = [
    { id: "trigger",  label: "What triggers it" },
    { id: "content",  label: "Memory content (detail, vividness)" },
    { id: "age",      label: "Age of the memory" },
    { id: "emotion",  label: "Emotion (valence, arousal, mixed)" },
    { id: "function", label: "Functions / well-being" },
    { id: "brain",    label: "Brain" },
    { id: "aging",    label: "Aging / clinical" },
    { id: "accuracy", label: "Accuracy / distortion" }
  ];

  // id, cite, mod[], out[], design, n, finding, caveat, doi
  var STUDIES = [
    { id: "wildschut2006", cite: "Wildschut et al. (2006)", mod: ["general"], out: ["trigger", "content", "emotion", "function"],
      design: "Seven studies (content analysis, triggers, functions)", n: "7 studies",
      finding: "Nostalgic narratives feature the self with close others and momentous events, hold more positive than negative affect, and often show negative scenes redeemed by later triumphs. Negative mood and loneliness trigger nostalgia; it bolsters social bonds, self-regard and positive affect.",
      caveat: "Mostly memories generated on request; Western samples.", doi: "10.1037/0022-3514.91.5.975" },

    { id: "reid2015", cite: "Reid et al. (2015)", mod: ["smell"], out: ["trigger", "emotion", "function"],
      design: "Participants sampled 12 scents and rated each", n: "n/r",
      finding: "Scents evoked more nostalgia the more arousing, familiar and autobiographically relevant they were, and in people high in nostalgia proneness. Scent-evoked nostalgia predicted positive affect, self-esteem, self-continuity, optimism, social connectedness and meaning, and carried more positive emotion than non-nostalgic memories.",
      caveat: "Correlational, scent-by-scent ratings; no other modality in the design.", doi: "10.1080/09658211.2013.876048" },

    { id: "herz2004", cite: "Herz (2004)", mod: ["smell", "visual", "music"], out: ["content", "emotion"],
      design: "Repeated measures: the same 3 cues (campfire, fresh-cut grass, popcorn) as odor, picture and sound", n: "n/r",
      finding: "Odor-cued memories were significantly more emotional and evocative than the same cue seen or heard. No differences in vividness or specificity.",
      caveat: "Only three cue items; self-report; prior experience with each cue mattered.", doi: "10.1093/chemse/bjh025" },

    { id: "herzschooler2002", cite: "Herz & Schooler (2002)", mod: ["smell", "visual"], out: ["emotion"],
      design: "Repeated measures: cue presented after the memory was first retrieved from its verbal label", n: "n/r",
      finding: "Memories recalled with the odor present were more emotional than with the same cue shown visually or named; odor memories also tended to feel more \"brought back\" to the event.",
      caveat: "Early naturalistic design; small cue set.", doi: "10.2307/1423672" },

    { id: "willander2006", cite: "Willander & Larsson (2006)", mod: ["smell", "visual"], out: ["age", "content"],
      design: "Between-subjects: one cue type each (word, picture or odor)", n: "93 older adults",
      finding: "Odor-cued memories came mostly from the first decade of life; word- and picture-cued memories peaked at ages 11–20. Odor memories felt more like being brought back in time and had been thought of less often.",
      caveat: "Older adults only; cue sets differed across modalities.", doi: "10.3758/bf03193837" },

    { id: "willander2007", cite: "Willander & Larsson (2007)", mod: ["smell"], out: ["age", "emotion"],
      design: "Between-subjects: odor only vs name only vs odor + name", n: "72 older adults",
      finding: "Telling people the odor's name attenuated the childhood peak and lowered pleasantness and \"brought back\" feelings. Odor-evoked memories were more emotionally arousing than verbally cued ones, beyond perceptual stimulation.",
      caveat: "Older adults only.", doi: "10.3758/bf03193499" },

    { id: "chu2002", cite: "Chu & Downes (2002)", mod: ["smell", "visual"], out: ["content", "emotion"],
      design: "Two experiments with double cuing (verbal label first, then odor, other odor, visual or label again)", n: "n/r",
      finding: "Odor-cued memories differed in qualitative ratings and contained more detail. Visual cues and incongruent odors reduced the detail recalled.",
      caveat: "Cuing procedure is unusual; detail coded from reports.", doi: "10.3758/bf03194952" },

    { id: "rubin1984", cite: "Rubin et al. (1984)", mod: ["smell", "visual"], out: ["content"],
      design: "Two experiments: odors vs photographs vs names of common objects", n: "n/r",
      finding: "Odor-evoked memories had been thought about and talked about less often beforehand. Little else differed consistently, though odors might evoke more pleasant, emotional memories.",
      caveat: "The first empirical test; many later effects were mixed.", doi: "10.2307/1422158" },

    { id: "debruijn2018", cite: "de Bruijn & Bender (2018)", mod: ["smell", "visual"], out: ["content"],
      design: "Lab experiment: childhood / non-childhood odors vs images as cues", n: "170",
      finding: "Childhood-related odors produced richer memories (vividness, detail, emotional intensity) than childhood-related images or unrelated cues. A LIWC analysis found no difference in affective content.",
      caveat: "Self-rated richness; childhood memories only.", doi: "10.1080/09658211.2017.1381744" },

    { id: "toffolo2012", cite: "Toffolo et al. (2012)", mod: ["smell", "music", "visual"], out: ["content", "emotion"],
      design: "Aversive film paired with odor, sound and visual triggers matched on intensity, valence, arousal and salience; recalled a week later", n: "70",
      finding: "Odor-evoked memories of an aversive event were more detailed, unpleasant and arousing than memories evoked by auditory triggers, but not than visual ones.",
      caveat: "Laboratory film, not real-life memories.", doi: "10.1080/02699931.2011.555475" },

    { id: "hacklander2019", cite: "Hackländer et al. (2019)", mod: ["smell"], out: ["trigger", "content", "emotion", "age"],
      design: "Review of methods, findings and theories", n: "review",
      finding: "Analyses the methods used to test the Proust effect, picks out the most stable findings and offers hypotheses; recommends moving from establishing the phenomenon to explaining its causes.",
      caveat: "Review; read it for methods and open questions.", doi: "10.3758/s13423-018-1545-3" },

    { id: "larsson2014", cite: "Larsson et al. (2014)", mod: ["smell"], out: ["content", "emotion", "age", "brain"],
      design: "Overview of behavioral and neural work", n: "review",
      finding: "Autobiographical odor memories differ from those cued by sight or sound. Key features summarised as LOVER: Limbic, Old, Vivid, Emotional, Rare.",
      caveat: "Perspective article; the acronym is a summary, not a law.", doi: "10.3389/fpsyg.2014.00312" },

    { id: "herz2004fmri", cite: "Herz et al. (2004)", mod: ["smell", "visual"], out: ["brain", "emotion"],
      design: "fMRI recall to a personally meaningful odor/visual cue vs a control cue", n: "5 females",
      finding: "Greater amygdala and hippocampal activation to the personally significant odor than to any other cue; behavioral emotion was also greatest for that odor.",
      caveat: "Five participants: treat as a pilot.", doi: "10.1016/j.neuropsychologia.2003.08.009" },

    { id: "arshamian2013", cite: "Arshamian et al. (2013)", mod: ["smell"], out: ["brain"],
      design: "fMRI: same odor-evoked memory cued by the odor vs its name", n: "n/r",
      finding: "Both cues activated autobiographical-recollection regions. Odor cues drove more medial temporal, visual-vividness and emotion-related activity; word cues drove more widespread prefrontal activity. Naming the memory also activated olfactory (piriform) areas.",
      caveat: "Participants were pre-screened for specific odor memories.", doi: "10.1016/j.neuropsychologia.2012.10.023" },

    { id: "elhaj2018", cite: "El Haj et al. (2018)", mod: ["smell", "music"], out: ["aging", "content"],
      design: "Mild Alzheimer's disease vs controls: memories after odor, music or neither", n: "n/r",
      finding: "In Alzheimer's disease, both odor and music improved specificity, emotional experience, mental time travel and retrieval time; retrieval time improved more with odor. Regression suggested less executive involvement after odor or music.",
      caveat: "Mild stage only; small clinical samples.", doi: "10.1093/chemse/bjx064" },

    { id: "glachet2019", cite: "Glachet & El Haj (2019)", mod: ["smell"], out: ["aging", "emotion", "content"],
      design: "Mild Alzheimer's disease vs controls: memories with vs without odor", n: "n/r",
      finding: "Odor exposure raised arousal, subjective reliving and positivity of memories, but only in the Alzheimer's participants, not in healthy controls.",
      caveat: "Depression symptoms were related to the odor-evoked emotion.", doi: "10.3390/brainsci9060135" },

    { id: "janata2007", cite: "Janata et al. (2007)", mod: ["music"], out: ["content", "emotion", "trigger"],
      design: "Lab and online: excerpts of popular music, questionnaires and written memory reports", n: "n/r",
      finding: "About 30% of song presentations evoked autobiographical memories, usually with strong, mostly positive emotion; nostalgia was the third most common emotion.",
      caveat: "Descriptive; song excerpts chosen from a corpus.", doi: "10.1080/09658210701734593" },

    { id: "janata2009", cite: "Janata (2009)", mod: ["music"], out: ["brain"],
      design: "fMRI with music excerpts from participants' childhoods", n: "n/r",
      finding: "Dorsal medial prefrontal cortex tracked how autobiographically salient each 30-s excerpt was, and acted with lateral prefrontal and posterior regions during familiar, salient songs.",
      caveat: "Young adults; correlational with salience ratings.", doi: "10.1093/cercor/bhp008" },

    { id: "barrett2010", cite: "Barrett et al. (2010)", mod: ["music"], out: ["trigger", "emotion"],
      design: "Participants rated nostalgia for randomly selected popular-music excerpts", n: "n/r",
      finding: "Nostalgia was stronger when a song was autobiographically salient, arousing and familiar, and when it evoked positive, negative and mixed emotions. Nostalgia proneness predicted stronger nostalgic experiences.",
      caveat: "Experimenter-selected songs.", doi: "10.1037/a0019006" },

    { id: "hennessy2024", cite: "Hennessy et al. (2024)", mod: ["music"], out: ["trigger", "emotion"],
      design: "Online survey: self-selected nostalgic songs vs musically matched familiar non-nostalgic songs", n: "582",
      finding: "Conceptual replication of Barrett et al.: nostalgic songs were rated higher in valence and arousal, and sometimes mixed valence, than matched familiar songs. Trait nostalgia predicted nostalgia ratings for both song types; personality shaped the affective profile.",
      caveat: "Online listening conditions; self-report.", doi: "10.1037/emo0001389" },

    { id: "hennessy2025", cite: "Hennessy et al. (2025)", mod: ["music"], out: ["brain", "aging"],
      design: "fMRI: personalized nostalgic, familiar non-nostalgic and unfamiliar songs matched for musical features (machine-learning matching)", n: "57 (29 aged 18–35; 28 aged 60+)",
      finding: "Nostalgic music, more than familiar or unfamiliar music, engaged default-mode, salience, reward and medial temporal regions, with self-referential and insula connectivity. Older adults showed stronger BOLD responses in nostalgia-related regions.",
      caveat: "Music only; cross-sectional age comparison.", doi: "10.1002/hbm.70181" },

    { id: "belfi2016", cite: "Belfi et al. (2016)", mod: ["music", "visual"], out: ["content"],
      design: "Memories evoked by 30 songs vs 30 famous faces, coded with the Autobiographical Interview", n: "n/r",
      finding: "Music-evoked memories were more vivid, with a greater proportion of internal details and more perceptual details; face-evoked memories had more external details. Women retrieved more vivid memories.",
      caveat: "Famous faces are a particular comparison cue.", doi: "10.1080/09658211.2015.1061012" },

    { id: "belfi2022", cite: "Belfi et al. (2022)", mod: ["music", "visual"], out: ["content"],
      design: "Music-evoked vs face-evoked memories, voluntary vs involuntary retrieval", n: "n/r",
      finding: "Music memories were more episodically rich and perceptually detailed than face memories regardless of whether retrieval was involuntary, so involuntariness alone does not explain music's advantage.",
      caveat: "Cue features (what else differs between songs and faces) remain unexplained.", doi: "10.1016/j.concog.2022.103305" },

    { id: "jakubowski2023", cite: "Jakubowski et al. (2023)", mod: ["music", "food"], out: ["content", "aging", "trigger"],
      design: "Two 4-day paper-diary periods, music vs food cues", n: "78 (39 young, 39 older)",
      finding: "Music triggered more frequent autobiographical memories, a larger share of involuntary memories and memories rated more personally important than food. Older adults recalled older, less specific memories that they rated as more positive, vivid and rehearsed.",
      caveat: "Self-recorded diaries; participants knew the topic.", doi: "10.1111/bjop.12639" },

    { id: "krumhansl2013", cite: "Krumhansl & Zupnick (2013)", mod: ["music"], out: ["age"],
      design: "Young adults rated top hits across 5.5 decades", n: "n/r",
      finding: "Memories, recognition, liking and emotion peaked for music from participants' own two decades — and also for their parents' generation (\"cascading reminiscence bumps\").",
      caveat: "Popular music; cultural context.", doi: "10.1177/0956797613486486" },

    { id: "jakubowski2020", cite: "Jakubowski et al. (2020)", mod: ["music"], out: ["age"],
      design: "Participants rated 111 chart songs from 1950–2015", n: "470 (ages 18–82)",
      finding: "A reminiscence bump in adolescence (peak around age 14) for autobiographical salience and familiarity of songs; liking showed a cascading bump from parents' adolescent years.",
      caveat: "Titles shown, not played.", doi: "10.1177/2059204320965058" },

    { id: "elhaj2012", cite: "El Haj et al. (2012)", mod: ["music"], out: ["aging", "content"],
      design: "Young adults, older adults and Alzheimer's patients recalled events after own chosen music vs silence", n: "n/r",
      finding: "Music-evoked memories were more specific, more emotional, retrieved faster and engaged less executive processing, which the authors read as involuntary-memory features.",
      caveat: "Participant-chosen music.", doi: "10.1016/j.concog.2011.12.005" },

    { id: "reid2023", cite: "Reid et al. (2023)", mod: ["food"], out: ["trigger", "emotion", "function"],
      design: "Three studies: visualise a nostalgic vs regular food, visualise 12 foods, taste 12 flavour samples", n: "n/r",
      finding: "Food is a powerful nostalgia elicitor with a contextual profile like other elicitors, but a predominantly positive emotional tone; it served positive affect, self-esteem, social connectedness and meaning functions.",
      caveat: "Self-report ratings.", doi: "10.1080/02699931.2022.2142525" },

    { id: "reid2026", cite: "Reid et al. (2026)", mod: ["food"], out: ["function"],
      design: "Four studies (two correlational; two preregistered experiments)", n: "n/r",
      finding: "Nostalgia for food experiences was linked to comfort; in the experiments this ran through stronger social connectedness.",
      caveat: "Recalled or visualised foods in experiments.", doi: "10.1080/02699931.2025.2479170" },

    { id: "vignolles2014", cite: "Vignolles & Pichon (2014)", mod: ["food"], out: ["trigger", "emotion"],
      design: "Qualitative analysis of 104 descriptions of nostalgic food consumption", n: "104 descriptions",
      finding: "Six themes (childhood, yearning, substitute, homesickness, special occasions, rediscovery); nostalgic food consumption was linked mainly to positive emotions.",
      caveat: "Exploratory, qualitative, marketing context.", doi: "10.1108/qmr-06-2012-0027" },

    { id: "troisi2011", cite: "Troisi & Gabriel (2011)", mod: ["food"], out: ["function"],
      design: "Two experiments on comfort food", n: "n/r",
      finding: "Comfort foods automatically activate relationship concepts and buffer belongingness threats in securely attached people (about comfort food, not nostalgia as such).",
      caveat: "Not a nostalgia study; useful for mechanism ideas.", doi: "10.1177/0956797611407931" },

    { id: "zhou2012", cite: "Zhou et al. (2012)", mod: ["temp", "music"], out: ["trigger", "function"],
      design: "Five studies (cold days and rooms, music-evoked nostalgia, recall tasks, cold-pressor)", n: "n/r",
      finding: "Coldness triggers nostalgia (colder days, a cold room), and nostalgia raises felt temperature and tolerance of noxious cold.",
      caveat: "Several small experiments; effects worth replicating.", doi: "10.1037/a0027236" },

    { id: "oba2016", cite: "Oba et al. (2016)", mod: ["visual"], out: ["brain"],
      design: "fMRI with childhood-related visual stimuli", n: "healthy females (n/r in abstract)",
      finding: "Nostalgia-related activity in hippocampus, substantia nigra/ventral tegmental area and ventral striatum; hippocampus–striatum co-activation scaled with individual nostalgia tendencies.",
      caveat: "Women only; correlational.", doi: "10.1093/scan/nsv073" },

    { id: "hu2025", cite: "Hu et al. (2025)", mod: ["multi", "music", "visual"], out: ["brain", "trigger"],
      design: "64-channel EEG, 3 × 2 within-subject (auditory, visual, audiovisual × nostalgic vs not)", n: "38 recruited (36 usable)",
      finding: "Nostalgic stimuli raised state nostalgia and altered alpha/gamma network measures. Auditory and audiovisual stimuli produced more state nostalgia than visual ones; the network measures did not differ by channel.",
      caveat: "The text I retrieved suggests a fixed presentation order and non-matched control stimuli; check the paper yourself. A good critical-reading exercise.", doi: "10.3389/fpsyg.2025.1517449" },

    { id: "yilmaz2025", cite: "Yılmaz-Özdemir et al. (2025)", mod: ["multi"], out: ["trigger", "function"],
      design: "Two experiments: VR nostalgia task vs event reflection task", n: "n/r",
      finding: "An augmented VR task produced stronger and longer-lasting felt nostalgia than the event reflection task; psychological benefits were similar across induction methods.",
      caveat: "Induction-method paper; no sensory-modality manipulation inside VR.", doi: "10.3758/s13428-025-02851-8" },

    { id: "zaragoza2026", cite: "Zaragoza Scherman et al. (2026)", mod: ["general"], out: ["trigger"],
      design: "Open-ended question \"What makes you feel nostalgic?\", coded for cue type", n: "256",
      finding: "Most frequently named cues were sensory and environmental: photographs, music, media, smells, conversations and food. Most responses reflected personal nostalgia.",
      caveat: "Descriptive; what people say triggers nostalgia may differ from what does.", doi: "10.1080/09658211.2026.2710049" },

    { id: "hepper2024", cite: "Hepper et al. (2024)", mod: ["general"], out: ["trigger", "function"],
      design: "Dispositional, self-reported triggers and induced nostalgia in 28 countries plus Hong Kong", n: "2,606 young adults",
      finding: "Nostalgia is common across cultures. Triggers: psychological threat (especially in warmer countries), sensory stimuli (especially in more-developed countries) and social gatherings (especially in less-developed countries). Nostalgic recall raised social connectedness, self-continuity and meaning everywhere.",
      caveat: "Young adults (mostly students).", doi: "10.1037/xge0001521" },

    { id: "newman2020", cite: "Newman et al. (2020)", mod: ["general"], out: ["emotion", "function"],
      design: "Scale development plus daily-life sampling studies and one induction comparison", n: "n/r",
      finding: "In daily life, state nostalgia was negatively related to well-being, with mixed same-day and negative next-day effects; induced recollections were rated more positively than everyday ones.",
      caveat: "Different measure (PINE); challenges the generality of lab benefits.", doi: "10.1037/pspp0000236" },

    { id: "leunissen2021", cite: "Leunissen et al. (2021)", mod: ["general"], out: ["emotion"],
      design: "Integrative data analysis of 41 nostalgia experiments", n: "4,659",
      finding: "Nostalgia inductions increased positive and ambivalent affect but did not significantly change negative affect; effect size varied markedly with the induction and the control condition.",
      caveat: "Hedonic character depends on how nostalgia is elicited.", doi: "10.1177/1754073920950455" },

    { id: "weingarten2026", cite: "Weingarten et al. (2026)", mod: ["general"], out: ["trigger", "function"],
      design: "Meta-analysis of nostalgia experiments", n: "347 experiments (benefits)",
      finding: "As reported in the repository abstract: benefits pooled g ≈ 0.39 (1,460 effect sizes, 347 experiments, 167 documents); threat as a trigger g ≈ 0.43. Check the paper before quoting.",
      caveat: "I could not open the full text; numbers come from the repository abstract.", doi: "10.1016/j.jesp.2026.104891" },

    { id: "ismail2018", cite: "Ismail et al. (2018)", mod: ["general", "music"], out: ["aging", "function"],
      design: "Three experiments with people with mild/moderate dementia (one used music)", n: "27, 29, 50",
      finding: "Nostalgia (vs control) raised social connectedness, meaning, self-continuity, optimism, self-esteem and positive affect, and nostalgic participants recalled more self-referent dementia-related information.",
      caveat: "Small clinical samples.", doi: "10.3233/jad-180075" },

    { id: "hepper2021", cite: "Hepper et al. (2021)", mod: ["general"], out: ["aging", "function"],
      design: "Four studies across the adult lifespan and time-horizon manipulations", n: "443 (ages 18–91) in Study 1",
      finding: "High-nostalgia-prone adults maintained wellbeing with age; limited-time perspectives triggered nostalgia, and nostalgic recall buffered the wellbeing cost of limited time.",
      caveat: "Cross-sectional age data in Study 1.", doi: "10.1037/emo0000728" },

    { id: "leboe2006", cite: "Leboe & Ansons (2006)", mod: ["general"], out: ["accuracy"],
      design: "Experiments manipulating encoding so some words supported more detailed recollection", n: "n/r",
      finding: "Rich recollection biased people to judge a prior encounter as emotionally positive, consistent with nostalgia partly reflecting a misattribution of successful remembering to a pleasant past.",
      caveat: "Word-list laboratory paradigm, not personal memories.", doi: "10.1037/1528-3542.6.4.596" },

    { id: "rogers2020", cite: "Rogers (2020)", mod: ["general"], out: ["accuracy", "emotion"],
      design: "Recall of nostalgic vs ordinary event from first- or third-person perspective", n: "409",
      finding: "The positive-affect advantage of nostalgic over ordinary recall appeared for first-person recall but not for third-person recall.",
      caveat: "Single study; perspective manipulated by instruction.", doi: "10.3389/fpsyg.2020.572345" },

    { id: "munawar2018", cite: "Munawar et al. (2018)", mod: ["general"], out: ["age"],
      design: "Systematic review of 68 quantitative studies", n: "68 studies",
      finding: "The reminiscence bump covers roughly ages 10–30 for important events, about 5–30 for word-cued memories and 6–39 for life-script studies; narrative/identity and cultural life-script accounts had the most support.",
      caveat: "Bump is for autobiographical memory in general, not nostalgia specifically.", doi: "10.1371/journal.pone.0208595" },

    { id: "wheeler2000", cite: "Wheeler et al. (2000)", mod: ["visual", "music"], out: ["brain", "content"],
      design: "fMRI recall test after learning pictures and sounds", n: "n/r",
      finding: "Vivid remembering reactivated sensory-specific cortex: visual regions for pictures, auditory regions for sounds, a subset of those active during perception.",
      caveat: "Newly learned lab items, not autobiographical memories.", doi: "10.1073/pnas.97.20.11125" },

    { id: "yang2022", cite: "Yang et al. (2022)", mod: ["general"], out: ["brain"],
      design: "Prospective review proposing a neural model", n: "review",
      finding: "Nostalgia should draw on self-reflection (mPFC, PCC, precuneus), autobiographical memory (hippocampus plus midline regions), emotion regulation (ACC, mPFC) and reward (striatum, SN/VTA, vmPFC). Only a handful of neural studies existed.",
      caveat: "A model to test, not a result.", doi: "10.1093/scan/nsac036" },

    { id: "levine2002", cite: "Levine et al. (2002)", mod: ["general"], out: ["content"],
      design: "Autobiographical Interview: scoring episodic vs semantic details", n: "method",
      finding: "Introduces a reliable scoring system separating internal (episodic) from external (semantic) details of recalled events; used by Belfi et al. (2016) for music-evoked memories.",
      caveat: "Needs trained, blind coders and transcribed recall.", doi: "10.1037/0882-7974.17.4.677" }
  ];

  // Seeds for RA research ideas (used by slides.html and workbook.html)
  var SEEDS = [
    { id: "q1", title: "Matched-cue showdown", level: "Medium–high",
      q: "When smell, music and image cues are matched for familiarity and personal relevance, do they differ in nostalgia intensity, memory richness and bittersweetness?",
      hook: "Modality comparisons exist for autobiographical memory in general (Herz, 2004; Belfi et al., 2016; Jakubowski et al., 2023), but familiarity and personal relevance drive nostalgia (Barrett et al., 2010; Reid et al., 2015) and usually differ across cues. In our (non-systematic) search we did not find a matched, self-selected, three-modality test with nostalgia as the outcome.",
      design: "Within-subjects: 3 modalities × (nostalgic vs familiar non-nostalgic cue), order counterbalanced (Latin square).",
      measures: "State nostalgia; mixed-emotion ratings; Autobiographical Interview internal details; \"brought back in time\" rating.",
      pitfalls: "Odor delivery and habituation; verbal labels (Willander & Larsson, 2007); order effects; keep a stimulus-selection session separate from the test session.",
      refs: ["herz2004", "belfi2016", "jakubowski2023", "barrett2010", "reid2015", "willander2007", "levine2002"] },
    { id: "q2", title: "How old is the nostalgic past, by sense?", level: "Low",
      q: "Do nostalgic memories cued through different senses come from different life periods (smell: childhood; music: adolescence)?",
      hook: "Odor-cued memories skew to the first decade (Willander & Larsson, 2006) while song salience peaks around adolescence (Jakubowski et al., 2020); the general bump is roughly 10–30 (Munawar et al., 2018). Whether the pattern holds for nostalgic memories specifically is open.",
      design: "Online study: participants date a nostalgic memory evoked by their own cue in each modality; compare with an ordinary memory.",
      measures: "Age at event; nostalgia rating; vividness; whether the cue was named or experienced.",
      pitfalls: "The cue's own age (a song released in 2012 cannot cue a 1998 memory); naming the cue changes the pattern.",
      refs: ["willander2006", "willander2007", "jakubowski2020", "krumhansl2013", "munawar2018"] },
    { id: "q3", title: "Rich or just rosy?", level: "Medium",
      q: "Are nostalgic memories richer in objective episodic detail than ordinary ones, or do they only feel richer?",
      hook: "Nostalgia may partly reflect the pleasant feeling of fluent remembering (Leboe & Ansons, 2006), and the positive-affect advantage depends on recall perspective (Rogers, 2020). Detail can be scored objectively with the Autobiographical Interview (Levine et al., 2002).",
      design: "Event reflection task (nostalgic vs ordinary event); blind coding of transcripts; optional check against an external record (a dated photo, a diary entry).",
      measures: "Internal vs external details; subjective vividness and reliving; word count as a covariate.",
      pitfalls: "Nostalgic memories may simply be older or longer; coders must be blind to condition.",
      refs: ["leboe2006", "rogers2020", "levine2002", "belfi2016"] },
    { id: "q4", title: "Lab nostalgia vs everyday nostalgia", level: "Medium",
      q: "Do cue-triggered nostalgic episodes in daily life differ from induced ones in valence, memory content and function?",
      hook: "Daily-life nostalgia related negatively to well-being while induced nostalgia is positive (Newman et al., 2020); diary work shows music memories are frequent and often involuntary (Jakubowski et al., 2023).",
      design: "7-day diary logging each nostalgic episode (cue modality, voluntary vs involuntary, age of memory, valence) plus one lab event-reflection session with the same people.",
      measures: "Valence, intensity, social content, well-being that day; the same ratings after the lab induction.",
      pitfalls: "Reactivity (logging changes behavior); compliance; privacy of memory content.",
      refs: ["newman2020", "jakubowski2023", "leunissen2021", "wildschut2006"] },
    { id: "q5", title: "Time capsule: plant the cue, test the nostalgia later", level: "High",
      q: "Does pairing a distinctive odor or song with an experience at encoding raise later nostalgia and memory detail when the cue returns?",
      hook: "Encoding specificity (Tulving & Thomson, 1973) predicts that matching cues help retrieval, and odor-evoked memory is thought to rest partly on associative learning (Herz, 2016). Nostalgia can also be anticipated (Cheung et al., 2020). Tests of planned cue–event pairing with nostalgia as the outcome are, as far as we found, rare.",
      design: "Day 1: a shared positive lab experience with ambient scent/music A or B; 1–2 weeks later re-expose to A or B (or neither), then free recall and nostalgia ratings.",
      measures: "Free recall detail; state nostalgia; social connectedness with the group.",
      pitfalls: "Novel scents are salient in themselves; need a large N for small effects; ethics and ventilation for scents.",
      refs: ["herz2004", "hacklander2019", "reid2015", "wheeler2000"] },
    { id: "q6", title: "Smell + sound", level: "High",
      q: "Do multisensory cues (scent plus music) produce more than the sum of their parts for nostalgia?",
      hook: "Channel comparisons exist for audio, visual and audiovisual stimuli (Hu et al., 2025) and immersive VR boosts felt nostalgia (Yılmaz-Özdemir et al., 2025), but scent plus music with personally relevant cues has not, to our knowledge, been tested.",
      design: "2 × 2: scent present/absent × music present/absent, personally relevant cues, counterbalanced.",
      measures: "State nostalgia; reliving; physiological arousal if available.",
      pitfalls: "Scent lingering between trials; interactions need larger samples than main effects.",
      refs: ["hu2025", "yilmaz2025", "reid2015", "barrett2010"] },
    { id: "q7", title: "Do the senses change with age?", level: "Medium–high",
      q: "Do cue-modality effects differ in younger vs older adults (and when memory is impaired)?",
      hook: "Odor boosted memory in Alzheimer's participants but not in healthy older controls (Glachet & El Haj, 2019); older adults recall older, less specific, more positive memories (Jakubowski et al., 2023) and show stronger responses to nostalgic music (Hennessy et al., 2025).",
      design: "Young vs older adults; same battery of personalized smell, music and image cues.",
      measures: "Nostalgia; Autobiographical Interview details; olfactory identification score as a covariate.",
      pitfalls: "Olfactory decline with age; cohort differences in music and media.",
      refs: ["glachet2019", "elhaj2018", "jakubowski2023", "hennessy2025", "hepper2021"] },
    { id: "q8", title: "Who is smell-nostalgic?", level: "Low–medium",
      q: "Do nostalgia proneness, imagery vividness and olfactory ability predict how much people feel nostalgic about scents?",
      hook: "Nostalgia proneness predicts scent-evoked and music-evoked nostalgia (Reid et al., 2015; Barrett et al., 2010; Hennessy et al., 2024); odor-memory effects may depend on prior experience with each odor (Herz, 2004).",
      design: "Correlational: trait nostalgia (Southampton Nostalgia Scale), imagery questionnaire, a short odor-identification test, then ratings of a scent set.",
      measures: "Scent-evoked nostalgia per scent; familiarity; autobiographical relevance.",
      pitfalls: "Scent set choice; culture- and region-specific familiarity; measurement of imagery by self-report.",
      refs: ["reid2015", "barrett2010", "hennessy2024", "herz2004"] }
  ];

  // Quiz bank (retrieval practice)
  var QUIZ = [
    { q: "In Willander & Larsson (2006), where did most odor-cued autobiographical memories come from?",
      opts: ["Early adulthood (ages 20–30)", "The first decade of life (under 10)", "The last 5 years", "Ages 11–20, like word and picture cues"], a: 1,
      why: "Odor-cued memories clustered in the first decade; word and picture cues peaked at 11–20. Willander & Larsson (2006)." },
    { q: "Herz (2004) compared the same cue as odor, picture and sound. Which result did it report?",
      opts: ["Odor memories were more emotional but not more vivid or specific", "Odor memories were more vivid and specific but not more emotional", "No differences at all", "Sound produced the most emotional memories"], a: 0,
      why: "More emotional and evocative for odor; no difference in vividness or specificity." },
    { q: "Which three properties of a scent or song predicted how nostalgic it made people feel (Reid et al., 2015; Barrett et al., 2010)?",
      opts: ["Loudness, length, price", "Arousal, familiarity and autobiographical relevance/salience", "Age, sex and country", "Brightness, color and shape"], a: 1,
      why: "Both studies found nostalgia rose with arousal, familiarity and autobiographical relevance (salience)." },
    { q: "Newman et al. (2020) found what about nostalgia in everyday life?",
      opts: ["It was strongly positive for well-being", "State nostalgia in daily life was negatively related to well-being", "It never occurs outside the lab", "It was identical to induced nostalgia"], a: 1,
      why: "Lab-induced recollections were rated more positively than daily-life nostalgia, which related negatively to well-being." },
    { q: "Leboe & Ansons (2006) argued that nostalgia may partly arise because...",
      opts: ["Memories become more accurate over time", "The pleasant feeling of successful remembering is misattributed to a pleasant past", "People forget negative events entirely", "Nostalgic people lie more"], a: 1,
      why: "Rich recollection biased judgments of the earlier encounter toward positive: a fluency misattribution account." },
    { q: "Belfi et al. (2022) asked whether music's episodic richness is explained by involuntary retrieval. What did they conclude?",
      opts: ["Yes, entirely", "No: music memories were richer than face memories even when both were involuntary", "Music memories were less rich", "They could not test it"], a: 1,
      why: "Involuntary retrieval alone does not explain the music advantage." },
    { q: "Roughly which ages does the reminiscence bump cover for important events (Munawar et al., 2018)?",
      opts: ["0–5", "10–30", "40–60", "60–80"], a: 1,
      why: "About 10–30 for important events; about 5–30 for word cues; 6–39 for life-script studies." },
    { q: "In Hepper et al. (2024), sensory stimuli as nostalgia triggers were especially common in...",
      opts: ["Warmer countries", "Less-developed countries", "More-developed countries", "Countries with older populations"], a: 2,
      why: "Threat triggers: warmer countries; sensory stimuli: more-developed countries; social gatherings: less-developed countries." },
    { q: "Zhou et al. (2012) linked nostalgia to temperature. Which pair is correct?",
      opts: ["Heat triggers nostalgia; nostalgia cools you down", "Cold triggers nostalgia; nostalgia raises felt warmth", "No link was found", "Nostalgia lowers pain tolerance"], a: 1,
      why: "Colder days and rooms raised nostalgia; nostalgia raised felt temperature and tolerance of noxious cold." },
    { q: "Glachet & El Haj (2019): in whom did odor exposure raise arousal, reliving and positivity of autobiographical memories?",
      opts: ["Healthy controls only", "Both groups equally", "Participants with Alzheimer's disease only", "Neither group"], a: 2,
      why: "The odor effect was seen only in the Alzheimer's group." },
    { q: "Which nostalgia-induction method is the standard comparison in many experiments?",
      opts: ["Free association", "Event reflection task with an ordinary-event control", "Viewing random photos", "Playing white noise"], a: 1,
      why: "The event reflection task (nostalgic vs ordinary event) is the most common induction, and VR inductions are compared against it (Yılmaz-Özdemir et al., 2025)." },
    { q: "Hackländer et al. (2019) ended their review of odor-evoked autobiographical memory by recommending that the field...",
      opts: ["Stop studying odors", "Shift from establishing the phenomenon to explaining its causes", "Only use clinical samples", "Use only self-report"], a: 1,
      why: "They call for explaining causes now that the basic phenomenon has been described." },
    { q: "Hennessy et al. (2025) fMRI: which networks were more active for personalized nostalgic music than for matched familiar or unfamiliar music?",
      opts: ["Default mode, salience, reward and medial temporal regions", "Only primary auditory cortex", "Only motor cortex", "Visual cortex"], a: 0,
      why: "Bilateral default-mode, salience, reward, medial temporal and supplementary motor activity." }
  ];

  // Vignettes for "spot the confound" (generic designs, written for teaching)
  var VIGNETTES = [
    { t: "Same order for everyone",
      d: "Every participant first looks at pictures, then listens to songs, then smells scents, rating nostalgia after each. The scent ratings are highest.",
      opts: ["Scent is the strongest nostalgia cue.", "Modality is confounded with order (fatigue, build-up, expectation); counterbalance the order.", "Nothing is wrong; the sample is large enough.", "Smell ratings are always inflated."], a: 1,
      why: "When every participant gets the same fixed order, modality and time are inseparable. Use a Latin square or randomize." },
    { t: "Different kinds of control cues",
      d: "Nostalgic cues are songs from the participant's teenage years. Control cues are songs that came out last month.",
      opts: ["Good control: they are different songs.", "Nostalgia is confounded with familiarity (and probably liking); use familiar, musically matched non-nostalgic songs.", "Controls should be silence.", "Controls are not needed."], a: 1,
      why: "Hennessy et al. (2024, 2025) matched nostalgic songs with familiar non-nostalgic songs so that familiarity did not masquerade as nostalgia." },
    { t: "Telling people what they smell",
      d: "In a smell condition the experimenter says \"this is the scent of freshly baked bread\" before participants sniff.",
      opts: ["Helpful: clearer instructions.", "Naming the odor can change the age and quality of the memories; keep odor-only and odor+name as separate conditions.", "It only affects smell-impaired people.", "It makes the odor weaker."], a: 1,
      why: "Willander & Larsson (2007): naming an odor attenuated the childhood peak and lowered pleasantness and \"brought back\" feelings." },
    { t: "One scent set for all",
      d: "Everyone smells the same five scents (vanilla, cut grass, pine, coffee, lavender); nostalgia is averaged across participants.",
      opts: ["Standardization is always best.", "Personal relevance and familiarity vary by person and region and predict nostalgia; measure them, or let people select cues.", "Averages remove all variation.", "Five scents is too few to analyze."], a: 1,
      why: "Reid et al. (2015): scents evoked more nostalgia as they were more familiar, arousing and autobiographically relevant." },
    { t: "No ordinary-event control",
      d: "Participants recall a nostalgic event, then rate their meaning in life. Compared with a pre-test, meaning increased.",
      opts: ["Nostalgia raises meaning in life.", "Without an ordinary-event (or similar) control you cannot separate nostalgia from recall, time, practice or demand.", "Pre-tests are never useful.", "Meaning in life cannot be measured."], a: 1,
      why: "Standard nostalgia experiments contrast nostalgic with ordinary-event recall, and the choice of control changes effect sizes (Leunissen et al., 2021)." },
    { t: "More detail means more accurate",
      d: "Nostalgic memories contained more words and sensory details than ordinary ones, so the authors say they are more accurate.",
      opts: ["Right: detail is accuracy.", "Detail is not accuracy; rich recall can raise confidence and pleasantness without being true. Compare with an external record.", "Word count is the best accuracy measure.", "Accuracy cannot be studied."], a: 1,
      why: "Leboe & Ansons (2006) show richness of recollection can bias judgments. Accuracy needs ground truth." },
    { t: "Five brains",
      d: "An fMRI study with five participants finds a larger amygdala response to the personally meaningful odor and concludes odors uniquely engage the amygdala.",
      opts: ["Strong proof.", "Treat as a pilot: tiny sample, so effects are imprecise and may not generalize; look for replication.", "Five is enough for fMRI.", "Amygdala responses are never reliable."], a: 1,
      why: "Herz et al. (2004) included five participants; the authors present it as converging evidence, not a final answer." },
    { t: "Students only",
      d: "A study of 18–22-year-olds concludes that \"odor cues bring back childhood memories across the lifespan\".",
      opts: ["Fine, since students are adults.", "The conclusion outruns the sample: age shapes which memories are recalled (older adults recall older, less specific memories).", "Students cannot have childhood memories.", "Sample age never matters."], a: 1,
      why: "Willander & Larsson (2006) used older adults; Jakubowski et al. (2023) found age differences in music- and food-evoked memories." }
  ];

  return { MODALITIES: MODALITIES, OUTCOMES: OUTCOMES, STUDIES: STUDIES, SEEDS: SEEDS, QUIZ: QUIZ, VIGNETTES: VIGNETTES };
})();
