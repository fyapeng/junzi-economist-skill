## Frontier judgment as of 2026-07-13

The frontier is no longer well described by a one-stage model in which patients freely choose among hospitals. The economically relevant sequence is:

```text
illness and initial access
        ↓
physician decides whether/where to refer
        ↓
patient sees a physician-filtered set of providers
        ↓
hospital capacity and acceptance rules alter the feasible set
        ↓
patient/physician choose among feasible options
        ↓
waiting, treatment intensity, outcomes, and future referral learning
```

Observed hospital shares therefore combine at least four latent objects:

1. patient preferences;
2. physician recommendations and incentives;
3. hospital acceptance or rationing;
4. congestion-dependent availability.

A demand model that assigns all four to patient utility will generally misinterpret substitution, quality preferences, and welfare.

## Mechanism map

| Mechanism | Decision-maker | Effect of tighter capacity | Distinguishing prediction |
|---|---|---|---|
| Patient waiting-cost avoidance | Patient | Patients substitute toward shorter queues, conditional on knowing them | Referral recommendation remains unchanged; patient’s final choice responds to independently disclosed waiting information |
| Physician clinical matching | Referring physician | Congestion matters only after clinical suitability and specialist capability | Referrals respond primarily to diagnosis–capability fit, not ownership or payment |
| Physician learning | Referring physician | Capacity limits how much referrals can be reallocated toward newly learned high-quality specialists | A physician’s own patients’ unexpected outcomes change later referrals, but only where the preferred specialist has slack |
| Relationship or habit persistence | Referring physician | Existing referral relationships absorb scarce slots; unfamiliar providers receive fewer referrals | Historical physician–provider ties predict referral after controlling for quality, distance, and current capacity |
| Financial incentives | Physician, insurer, hospital | Scarce capacity is steered toward patients or hospitals with favorable reimbursement | Referral changes follow payment or ownership changes among clinically similar patients |
| Digital or organizational convenience | Physician or health system | Capacity within a shared EHR or integrated system is easier to observe and use | EHR or organizational boundaries redirect referrals without corresponding quality changes |
| Hospital rationing | Receiving hospital | Hospitals delay, reject, transfer, or reduce effort for marginal patients | Given the same physician recommendation, acceptance or treatment changes with occupancy |
| Risk selection or cream-skimming | Receiving hospital/system | Scarce slots are reserved for profitable or less costly cases | Acceptance varies with predicted profitability after conditioning on clinical need |
| Dynamic capacity investment | Hospital/system | Persistent inflows induce beds, staffing, entry, or specialization | Referral shocks change later capacity; short-run substitution differs from long-run equilibrium |
| Congestion externality | Entire network | A referral into one hospital changes treatment conditions for other patients | Capacity shocks affect outcomes of patients already inside the receiving hospital |
| Unequal rationing | Providers and institutions | Scarcity magnifies differences in waiting or provider effort across groups | Group-specific outcomes diverge at high occupancy despite similar measured need |

The central unresolved question is not whether distance, quality, and waiting matter. It is:

> When observed flows change, how much reflects patient valuation, physician agency, hospital feasibility, and strategic allocation of scarce capacity?

## Major competing explanations

### 1. Choice expands quality-responsive demand

The strongest foundational evidence is the English NHS choice reform. Gaynor, Propper, and Seiler explicitly model constrained consideration sets and find that removing choice restrictions increased responsiveness to clinical quality; their model attributes modest mortality and substantial patient-welfare gains to the reform. The same paper finds evidence of a hospital quality response.[AEA article and replication-material page](https://www.aeaweb.org/articles?id=10.1257/aer.20121532)

Boundary: this does not establish that patients normally face complete choice sets. Its leverage comes precisely from modeling and changing those constraints.

### 2. Physicians act as informed agents

Clinical matching may explain why patients do not attend the nearest hospital and why complex cases concentrate at capable centers. Under this account, referral networks improve allocation because physicians possess information patients lack.

The strongest challenge is that physician recommendations may reflect multiple objectives. Beckert’s two-stage model of English elective referrals treats the GP as both patient adviser and agent of the health authority. It finds that the GP preselects options using quality and financial considerations, while patients subsequently emphasize more tangible hospital attributes.[Journal of Health Economics article](https://doi.org/10.1016/j.jhealeco.2018.06.003)

### 3. Physicians respond to financial incentives

Ho and Pakes estimate hospital referrals for privately insured births in California. Plans with more capitated physicians are more price-responsive and send patients farther to lower-priced, similar-quality hospitals.[NBER Working Paper 19333 and published-version record](https://www.nber.org/papers/w19333)

This evidence rejects the interpretation that all referral variation reveals patient preferences. It does not imply that financial incentives always worsen matching: the reported pattern lowered prices without an estimated quality reduction, while increasing travel.

### 4. Referrals reflect learning—but learning is slow and capacity-limited

McCarthy and Richards-Shubik study 4.5 million Medicare joint-replacement surgeries. Their current working-paper abstract reports design-based evidence that PCPs respond to outcomes of their own referred patients. Their structural model incorporates habit persistence and capacity constraints and estimates that removing informational frictions would redirect about one-quarter of patients, with small but meaningful outcome improvements.[Current author working-paper page](https://www.ianmccarthyecon.com/research/working-papers/physician-learning/)

The competing interpretation is relationship persistence: physicians may continue using familiar specialists even after quality information changes. Capacity further means that a “send everyone to the best specialist” counterfactual is infeasible.

### 5. Infrastructure and organizational boundaries redirect referrals

Xue and Meyerhoefer exploit switches in EHR developers by affiliated hospitals. Their NBER abstract reports that PCP referrals to same-developer specialists rise by 5.8% after a switch, while referrals to specialists using the prior developer fall by 4.2%. Referrals to the PCP’s most frequently used specialists do not change, suggesting that digital convenience and durable relationships operate simultaneously.[NBER Working Paper 33861](https://www.nber.org/papers/w33861)

Whaley and Zhao find that physician–hospital integration redirects patients toward higher-priced hospital facilities; their model predicts higher Medicare spending under universal PCP integration.[Journal of Public Economics article](https://doi.org/10.1016/j.jpubeco.2024.105175)

These studies imply that observed referral networks can reflect interoperability and ownership rather than clinical quality.

### 6. Capacity changes outcomes, not merely waiting disutility

Godøy and coauthors use variation in orthopedic-surgery queue congestion. They find no increase in subsequent health-care utilization from longer waits, but persistent reductions in labor supply and increased disability receipt, concentrated among patients already on sick leave when referred.[AEJ: Economic Policy article and replication page](https://www.aeaweb.org/articles?id=10.1257/pol.20210399)

Singh and Venkataramani find that mortality rises for Black but not White patients as a hospital system approaches capacity. Their latest paper attributes the divergence to waiting and provider-effort rationing and reports that differential patient selection does not explain it.[April 2026 NBER PDF](https://www.nber.org/system/files/working_papers/w30380/w30380.pdf)

Capacity therefore changes treatment production and distribution. It cannot safely be represented only as a queue length observed by prospective patients.

### 7. New capacity can redirect flows without improving final outcomes

Arnold, Richards, and Whaley study psychiatric inpatient facility entry. Their abstract reports roughly 60% fewer psychiatric admissions at general hospitals and 50% more discharges to psychiatric facilities, but no short-run decline in emergency-department volume, community crime, overdose deaths, or suicides.[NBER Working Paper 34772](https://www.nber.org/papers/w34772)

This is important null evidence: successful diversion and specialization need not improve the final social outcomes used to justify capacity expansion.

## Contradictory and null evidence

The literature does not support a single monotonic claim that more choice or more capacity is always beneficial:

- Greater formal choice increased quality responsiveness in the English reform, but GP filtering means formal entitlement is not equivalent to an unrestricted patient choice set.
- Capitation redirected patients toward lower-priced hospitals without an estimated quality loss, whereas physician–hospital integration redirects patients toward higher-priced facilities.
- Longer surgical waits did not increase subsequent medical utilization in the Norwegian study, although they reduced labor supply.
- Psychiatric specialty-hospital entry sharply changed referral and discharge patterns but did not reduce several short-run community harms.
- Capacity strain can have highly unequal consequences; an average mortality or waiting-time effect can conceal group-specific rationing.
- The latest physician-learning work suggests better information could improve allocation, but habit persistence and specialist capacity sharply limit feasible reallocation.

These are not mutually invalidating results. They show that the sign of a policy effect depends on who controls the referral, what capacity is scarce, whether prices are regulated, and which outcome defines welfare.

## Compact claim-level source matrix

All retrievals occurred on **2026-07-13**. “Latest revision unknown” means the authoritative page inspected did not report one; it does not mean no revision exists.

| Source | Claim supported | Claim not supported | First issue/publication | Latest revision known | Status inspected |
|---|---|---|---|---|---|
| Gaynor, Propper & Seiler, “Free to Choose?” AER | Removing NHS choice restrictions increased quality responsiveness in that setting; model-implied mortality and welfare gains | Universal claim that unrestricted choice always raises welfare | Nov. 2016 | None reported | **abstract-verified**, publisher metadata; replication link verified |
| Ho & Pakes, “Hospital Choices, Hospital Prices and Financial Incentives to Physicians” | Physician/insurer payment incentives affect hospital referrals | Patient preferences alone explain hospital shares | NBER Aug. 2013; AER Dec. 2014 | NBER Mar. 2014 | **abstract-verified**, NBER metadata |
| Beckert, “Choice in the Presence of Experts” | Strategic GP preselection can bias one-stage patient-choice estimation | Every GP recommendation is financially distorted | Journal issue July 2018; earlier IFS WP 2016 | Unknown | **abstract-verified**, DOI/publisher metadata |
| McCarthy & Richards-Shubik, “Learning and the Efficiency of Physician Referrals” | PCPs learn from own-patient outcomes; habit and capacity constrain reallocation | Final causal or welfare magnitudes are publication-settled | Earliest public version located Sept. 2024 | Current author page dated July 2026 | **abstract-verified**; current status “under review”; version lineage partly verified |
| Xue & Meyerhoefer, “Effects of Switching EHR Developer…” | EHR compatibility causally shifts referral links under the paper’s design | EHR compatibility improves clinical matching or welfare | NBER May 2025; earlier AEA conference version Jan. 2023 | None reported by NBER | **abstract-verified**, NBER metadata; earlier conference metadata verified |
| Whaley & Zhao, “Effects of Physician Vertical Integration…” | Integration redirects referrals toward higher-priced facilities and raises model-implied Medicare spending | Integration necessarily harms clinical outcomes | Journal of Public Economics, vol. 238, 2024 | None reported | **abstract-verified**, publisher metadata |
| Godøy et al., “Hospital Queues, Patient Health, and Labor Supply” | Longer waits cause persistent labor-supply losses in the studied Norwegian margin | Longer waits increase all measured health utilization | May 2024 | None reported | **abstract-verified**, publisher metadata; replication link verified |
| Singh & Venkataramani, “Rationing by Race” | Capacity strain is associated with unequal mortality, waiting, and effort rationing under the paper’s design | All hospitals or capacity shocks generate the same disparity | NBER Aug. 2022 | 15 Apr. 2026 | **full-text-verified** for current NBER PDF/version header; SSRN revision metadata cross-checked |
| Arnold, Richards & Whaley, “Stress Relief?” | Psychiatric facility entry redirects admissions and discharges; several community outcomes show no short-run improvement | No long-run or patient-level benefit exists | NBER Jan. 2026 | None reported | **abstract-verified**, NBER metadata |
| NHS England, “Diversion of Referrals” | Capacity alerts visibly enter the GP/patient referral interface | Reported early-adopter changes are causal estimates | Initial page date not displayed | Unknown | **official-text-verified** |
| China NHC, 国卫办医政发〔2024〕21号 | China requires local referral rules and reserved outpatient/inpatient capacity for referred patients | Uniform implementation or causal effectiveness across regions | 27 Nov. 2024 | No revision identified | **official-text-verified** |

A version discrepancy is worth noting: the NBER landing page for “Rationing by Race” still displayed a May 2024 revision field during retrieval, while the current PDF header and SSRN record report an April 2026 revision. I use the current PDF’s **April 2026** version date.

## Three discriminating research designs

### Design 1: Referral recommendation × real-time capacity × final hospital choice

**Question:** Does congestion change physician recommendations, patient choice, or hospital acceptance?

Required linked data:

- initial diagnosis and severity;
- referring physician;
- complete recommendation or shortlist;
- capacity visible to the physician and patient at referral time;
- hospital acceptance or rejection;
- final hospital, waiting time, treatment, and outcome.

Use high-frequency, plausibly exogenous capacity shocks—such as unrelated emergency inflows or temporary unit closures—to estimate three margins separately:

1. effect on the physician’s recommended set;
2. effect on hospital acceptance, conditional on recommendation;
3. effect on patient choice, conditional on recommendation and availability.

Predictions:

- **Patient waiting-cost mechanism:** recommendations remain stable; patients substitute.
- **Physician congestion avoidance:** recommendations change immediately.
- **Hospital rationing:** recommendations remain stable, but acceptance changes.
- **Strategic selection:** acceptance changes differentially by predicted cost or reimbursement.

Main threat: emergency surges may change treatment conditions directly. They should not be used as instruments for final outcomes without modeling that direct congestion channel.

### Design 2: Capacity-alert threshold or rollout experiment

NHS England places red/green capacity information directly into the e-Referral interface seen by GPs and patients.[Official NHS capacity-alert description](https://www.england.nhs.uk/elective-care/best-practice-solutions/diversion-of-referrals/)

A credible design could exploit:

- phased rollout across referral areas;
- discontinuous alert thresholds;
- randomized or quasi-random presentation of capacity information;
- delayed updating that creates differences between displayed and actual congestion.

Outcomes should include the shortlist, final choice, waiting, travel, clinical matching, and outcomes—not merely referral volume.

Distinguishing predictions:

- **Information mechanism:** displayed status matters even conditional on actual occupancy.
- **True capacity mechanism:** actual occupancy matters beyond the displayed label.
- **Physician agency:** the response is concentrated in GP-generated shortlists.
- **Patient preference:** patients override recommendations when given direct access to alerts.

Failure condition: if alert thresholds are manually manipulated in response to unobserved quality or staffing problems, a simple regression discontinuity is invalid.

### Design 3: Reserved referral slots as a network-capacity intervention

China’s 2024 national notice requires higher-level hospitals to reserve some outpatient appointments and beds for referred patients, while local authorities and medical alliances develop referral rules.[Official NHC notice](https://www.nhc.gov.cn/yzygj/c100068/202411/d85d3ba36c43460fa67deb333f52203b.shtml)

Use staggered implementation across medical alliances, specialties, or disease directories, linking:

- primary-care encounters;
- referral applications;
- reserved-slot availability;
- receiving-hospital decisions;
- self-directed hospital attendance;
- treatment and longitudinal outcomes.

Estimate separately:

1. whether reserved capacity increases clinically appropriate upward referral;
2. whether it crowds out non-referred patients;
3. whether it reduces waiting or merely relocates it;
4. whether lower-level hospitals lose cases needed for capability accumulation;
5. whether high-cost patients are selectively transferred.

Mechanism tests:

- **Capability constraint:** effects concentrate where the referring hospital lacks the required service.
- **Financial risk transfer:** effects concentrate in predicted-loss cases, conditional on capability.
- **Access improvement:** previously constrained patients gain treatment without equivalent crowd-out.
- **network capture:** flows increase mainly toward the alliance’s lead hospital without better matching or outcomes.

A structural extension is justified only after these margins are identified. It should model physician recommendation, hospital acceptance, and patient choice as separate decisions with capacity as a state variable.

## Search log

Primary queries included:

- `hospital patient choice physician referral capacity constraints economics 2024 2025 2026 working paper`
- `site:nber.org/papers hospital referral capacity constraints patient choice 2025 OR 2026`
- `site:aeaweb.org hospital queues patient choice physician referral capacity`
- `site:england.nhs.uk capacity alerts referral patient choice official`
- `"Learning and the Efficiency of Physician Referrals" September 2024`
- `"Rationing by Race" April 2026 revision`
- `"Effects of Switching Electronic Health Record Developer" revision date`
- DOI/title searches for the Beckert and Whaley–Zhao articles

Sources searched included AEA, NBER, publisher DOI pages, author working-paper pages, NHS England, and China’s National Health Commission. Search-result pages and secondary summaries were not used as claim support.

## Stop reason

I stopped because each live mechanism now has:

- foundational evidence;
- at least one recent paper or working paper;
- an identified competing explanation;
- null or contradictory evidence;
- an official institutional setting capable of generating discriminating variation.

Additional searches were increasingly returning variants of the same five mechanisms—quality information, physician incentives, organizational ties, capacity rationing, and dynamic adjustment—and were no longer changing the proposed designs.

This is not an exhaustive bibliography. Important remaining lanes include emergency ambulance allocation, insurer network design, low- and middle-income-country referral systems outside China, and clinical operations research. I would reopen the search if:

- the July 2026 physician-learning paper releases a new full manuscript;
- “Rationing by Race” moves from forthcoming to a final AER version;
- the Chinese reserved-capacity policy produces implementation microdata;
- a new paper jointly observes recommendation sets, hospital rejection, and real-time capacity.
