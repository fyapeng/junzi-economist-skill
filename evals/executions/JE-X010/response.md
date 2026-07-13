## Verification scope

As-of date: **2026-07-13**.  
Research decision: whether these four sources jointly support a design that separates physician referral, patient response, and hospital capacity rationing.

Dates below are kept distinct. “Unknown” means the inspected artifact did not state the date; I do not substitute a copyright year, search-engine date, retrieval date, or webpage footer.

## Compact frontier ledger

### 1. Singh and Venkataramani, *Rationing by Race*

- **Stable identifier:** NBER Working Paper 30380; DOI [10.3386/w30380](https://doi.org/10.3386/w30380).
- **Publication status:** NBER working paper; an author publication page currently describes it as forthcoming in the *American Economic Review*, but a final AER article was not inspected.
- **First issue date:** **August 2022** on the [NBER landing page](https://www.nber.org/papers/w30380); the version list gives **2022-08-17** as the earliest downloadable version.
- **Document/effective date:** Current PDF header states **“August 2022, Revised April 2026.”** No “effective date” applies to a manuscript.
- **Webpage publication date:** **Unknown.** The NBER landing page does not expose a separate webpage-publication date.
- **Latest manuscript revision:** **April 2026** according to the [current NBER PDF](https://www.nber.org/system/files/working_papers/w30380/w30380.pdf); SSRN records **2026-04-15** as its last revision.
- **Conflicting authoritative surfaces:** During inspection, the NBER landing page still displayed **Revision Date May 2024**, while the PDF served from its current-file URL states **Revised April 2026**. The current PDF is the artifact used for substantive claims; the landing-page discrepancy is preserved rather than collapsed.
- **Retrieval timestamp:** **2026-07-13T09:33:36.594+08:00** for the current PDF.
- **Exact artifact inspected:** Current 69-page NBER PDF at the URL above; NBER landing-page metadata; SSRN revision metadata.
- **SHA-256 of current PDF bytes:** `F1A5345821CDA6BF9DDC7D8B7E8D27341EB30F102D16B1DA00C34DCD667CCC85`
- **Verification level:** **full-text-verified** for the current PDF and version header; metadata cross-checked.
- **Claim supported:** In the studied two-hospital health system, increasing capacity strain is associated with higher in-hospital mortality for Black but not White patients; the paper presents waiting time and provider effort as rationing channels and reports evidence against differential patient selection as the explanation.
- **Claim not supported:** Capacity strain necessarily produces the same racial disparity in other hospitals, specialties, periods, or countries; nor does the paper identify the effect of prospective patient choice or physician referral on congestion.

### 2. McCarthy and Richards-Shubik, *Learning and the Efficiency of Physician Referrals*

- **Stable identifier:** No DOI or archival working-paper number was located. Current authoritative surface: [Ian McCarthy’s project page](https://www.ianmccarthyecon.com/research/working-papers/physician-learning/).
- **Publication status:** **Under review**, according to the current author page.
- **First issue date:** **Unknown.** A cached earlier author-page surface displayed September 2024, and Seth Richards-Shubik’s institutional page lists a January 2025 version, but neither establishes the first public issue date of a stable manuscript. I therefore do not promote either to “first issue.”
- **Document/effective date:** The current author page displays **“Published July 2026.”** This is recorded as an author-supplied project-page date, not as a verified manuscript date. No policy effective date applies.
- **Webpage publication date:** **Unknown.** The page does not expose a distinct original webpage-publication date.
- **Latest manuscript revision:** **Unknown.** No manuscript PDF or explicit revision history was linked from the inspected page.
- **Conflicting authoritative surfaces:** Earlier indexed author-page content used the title *Learning and Efficiency in the Market for Physician Referrals* and displayed September 2024; the current page uses *Learning and the Efficiency of Physician Referrals* and displays July 2026. A Johns Hopkins coauthor page lists January 2025. These may represent successive project versions, but no inspected revision ledger connects them.
- **Retrieval timestamp:** **2026-07-13T09:33:45.240+08:00**
- **Exact artifact inspected:** Current author-page HTML containing title, authors, status, July 2026 display date, abstract, and code link. No manuscript PDF was available on that page.
- **SHA-256 of retrieved author-page HTML:** `ADD1749D6ED2D7D0AD539A9F594E6BC5BB21F668423D727C198AFD4E67E621F9`
- **Verification level:** **abstract-verified**; manuscript results and derivations are not full-text verified.
- **Claim supported:** The current abstract reports that PCPs update referrals in response to outcomes of their own patients and that the authors’ structural model incorporates habit persistence and specialist capacity constraints; its counterfactual suggests information frictions matter for referral allocation.
- **Claim not supported:** The inspected evidence does not establish that its structural parameters are independently identified, that the reported counterfactual has passed external validation, or that simply informing physicians would improve welfare at scale. Those claims require the unavailable manuscript and validation details.

### 3. China NHC, 国卫办医政发〔2024〕21号

- **Title:** 《关于加强首诊和转诊服务 提升医疗服务连续性的通知》
- **Issuers:** 国家卫生健康委办公厅、国家中医药局综合司、国家疾控局综合司.
- **Official source:** [National Health Commission policy page](https://www.nhc.gov.cn/yzygj/c100068/202411/d85d3ba36c43460fa67deb333f52203b.shtml).
- **First issue date:** **2024-10-28**, the date printed beneath the issuing authorities.
- **Document/effective date:** Document date **2024-10-28**; a distinct legal effective date is **not stated**.
- **Webpage publication date:** **2024-11-27**, explicitly displayed as `发布时间`.
- **Latest manuscript revision:** Not applicable; no amendment or revised version was identified on the inspected official page.
- **Retrieval timestamp:** Official text re-retrieved at **2026-07-13T09:34:32.128+08:00**.
- **Exact artifact inspected:** Official NHC HTML policy text, including document number, issuing authorities, printed document date, webpage publication date, objectives, referral rules, reserved-capacity requirement, and implementation instructions.
- **SHA-256:** Not available. Direct byte retrieval returned HTTP 412, although the official text was successfully inspected through the web retrieval interface. I do not hash a reconstructed rendering.
- **Verification level:** **official-text-verified**.
- **Claim supported:** The document requires locally specified referral rules; physician-initiated referral with patient informed consent; referral centers or designated departments; and higher-level hospitals reserving some outpatient appointments and inpatient beds for primary-care referrals. It sets staged targets for referral-system construction through 2025, 2027, and 2030.
- **Claim not supported:** The notice does not prove uniform local implementation, the amount of capacity actually reserved, compliance, causal effects on waiting or outcomes, or that referral flows observed after 2024 were caused by this notice.

### 4. NHS England, *Diversion of Referrals*

- **Official source:** [NHS England page](https://www.england.nhs.uk/elective-care/best-practice-solutions/diversion-of-referrals/).
- **First issue date:** **Unknown.**
- **Document/effective date:** **Unknown.** The page describes an operational programme and capacity-alert mechanism but states no document date or effective date.
- **Webpage publication date:** **Unknown.** No publication field was displayed in the page or located in the retrieved HTML metadata.
- **Latest manuscript revision:** Not applicable; latest webpage-update date is also **unknown**.
- **Retrieval timestamp:** **2026-07-13T09:34:02.896+08:00**
- **Exact artifact inspected:** Current NHS England HTML page describing red/green capacity alerts in the NHS e-Referral Service, their visibility to GPs and patients, reported early-adopter referral changes, and the offer of alternative providers for long-waiting patients.
- **SHA-256 of retrieved HTML:** `59A511495A3414D83CBCECC1C46B204EB47ECB4E02092D9973203F0F076974DC`
- **Verification level:** **official-text-verified**.
- **Claim supported:** NHS England describes a mechanism in which provider capacity status is displayed within the referral interface and can therefore enter the information set of both referring GPs and patients. The page reports reductions of up to 38% in referrals to red-flagged services and increases of up to 14% to green-flagged services at two early-adopter sites.
- **Claim not supported:** The early-adopter figures are not presented as estimates from a stated causal design. The page does not establish that the alerts improved clinical matching, reduced system-wide waiting, improved health, or caused the reported referral changes independently of concurrent operational interventions.

## Smallest joint mechanism map

These sources jointly motivate a three-stage allocation mechanism:

```text
Physician information and beliefs
        ↓
Referral recommendation / shortlist
        ↓
Displayed or reserved hospital capacity
        ↓
Hospital acceptance, waiting, and provider effort
        ↓
Patient allocation and outcomes
```

Only three mechanism families are needed:

1. **Referral learning and habit:** Physicians update beliefs about specialist quality, but prior relationships and capacity constrain feasible reallocation.
2. **Capacity-mediated choice:** Capacity information or reserved slots alter the choice set available at referral; observed hospital choice is therefore not pure patient preference.
3. **Capacity rationing after arrival:** When demand approaches capacity, hospitals may alter waiting and provider effort, potentially with unequal consequences across patients.

The sources do not establish a single causal chain connecting all three stages. In particular, the McCarthy–Richards-Shubik manuscript was not available for full-text verification, and the two official policies document institutional mechanisms rather than causal effects.

## One jointly motivated research design

### Linked referral–capacity–acceptance design

Construct patient-level data linking:

- initial diagnosis and severity;
- referring physician;
- recommended hospital set;
- capacity information displayed to the physician and patient;
- reserved referral slots;
- hospital acceptance or rejection;
- realized waiting, treatment effort, transfer, and outcome.

Exploit staggered introduction or threshold changes in capacity alerts or reserved referral slots. Estimate three effects separately:

1. **Recommendation effect:** Does capacity information change which hospitals physicians recommend?
2. **Acceptance effect:** Conditional on recommendation, does actual capacity change hospital acceptance, delay, or transfer?
3. **Rationing effect:** Conditional on arrival and measured need, does high strain change waiting, effort, and outcomes differently across patient groups?

This separates the mechanisms:

- If recommendations change when displayed capacity changes but hospital acceptance does not, the main channel is physician steering.
- If recommendations remain stable but acceptance changes with actual capacity, the channel is hospital rationing.
- If displayed status changes behavior independently of actual occupancy, information matters.
- If group-specific treatment or outcomes diverge only after arrival at high strain, unequal rationing—not patient choice—becomes the relevant margin.

The design fails if capacity labels or reserved slots are assigned in response to unobserved quality deterioration, staffing shocks, or expected patient severity and no independent variation is available. A rollout label alone does not solve that problem.

## Stop and reopening rule

**Decision-linked stop:** These four sources are sufficiently verified to motivate the linked referral–capacity–acceptance design and to reject a one-stage patient-choice interpretation. Further searching among these same four surfaces is unlikely to change that design today. It would mainly repeat the unresolved provenance problem for the physician-learning paper or the missing date metadata for the NHS page.

**Reopen when any of the following occurs:**

- a dated full manuscript or archival repository version of the McCarthy–Richards-Shubik paper becomes available;
- NBER or AEA publishes a final version of *Rationing by Race* that supersedes the April 2026 PDF;
- China releases implementation data or local rules quantifying reserved slots and rollout dates;
- NHS England supplies a dated evaluation, protocol, or microdata documentation for capacity alerts;
- a dataset becomes available that jointly observes physician recommendations, displayed capacity, hospital rejection, and post-arrival treatment.
