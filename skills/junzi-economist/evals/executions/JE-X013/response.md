## Research judgment as of 2026-07-13

The proposed economic object should be rejected in its current form.

A 30-day all-cause readmission indicator is not a direct monotone measure of hospital quality. It is a claims-generated event jointly determined by index-hospital care, survival, planned treatment, patient health, post-acute and outpatient access, hospital admission status, coding, selection, and the chosen observation window. Medicare’s payment rule also does not simply penalize a hospital-wide all-cause readmission rate: HRRP currently uses six condition- or procedure-specific, risk-standardized **unplanned** readmission measures; the hospital-wide measure belongs to the Hospital Inpatient Quality Reporting program, not HRRP.[CMS HRRP](https://www.cms.gov/medicare/quality/value-based-programs/hospital-readmissions)

The defensible research object is therefore:

> How do readmission penalties change hospitals’ multidimensional care, classification, selection, and transition-management decisions, and what are the resulting effects on survival, acute-care use, time at home, costs, and distribution?

## Minimal baseline economic model

Let hospital \(h\) choose costly quality \(q_h\geq 0\). A discharged patient is readmitted within 30 days with probability

\[
r_h(q_h), \qquad r'_h(q_h)<0,
\]

and quality costs \(c_h(q_h)\), with \(c'_h>0\) and \(c''_h>0\).

Let the hospital face penalty price \(\phi_h\) per unit of measured readmission risk. Its reduced-form objective is

\[
\Pi_h(q_h)
=
P_h-c_h(q_h)-\phi_h r_h(q_h).
\]

An interior optimum satisfies

\[
c'_h(q_h^*)=-\phi_h r'_h(q_h^*).
\]

Hence a larger penalty raises quality if the solution remains interior:

\[
\frac{\partial q_h^*}{\partial \phi_h}>0.
\]

If avoiding a readmission creates social benefit \(B\), baseline welfare is

\[
W_h(q_h)= -c_h(q_h)-B r_h(q_h),
\]

so a penalty equal to the marginal social harm, \(\phi_h=B\), implements the social optimum.

This result requires all of the following:

1. readmission is the relevant harmful event;
2. every counted readmission is negatively related to quality;
3. \(q\) is the only hospital response;
4. readmission status is measured without strategic classification;
5. death and other returns to acute care do not compete with readmission;
6. the hospital controls the relevant post-discharge process;
7. the penalty equals social marginal harm;
8. distribution and access consequences are absent.

The outside evidence defeats several of these assumptions.

## How outside evidence changes the model

### 1. Agents: quality is produced across organizations

The baseline contains only the index hospital. The relevant agents are instead:

- the patient and informal caregivers;
- the index hospital and its inpatient clinicians;
- emergency departments and observation units;
- primary-care and specialist physicians;
- skilled-nursing, rehabilitation, home-health, hospice, and other post-acute providers;
- Medicare, which defines the measure and penalty;
- hospital coding, utilization-review, and discharge-management functions.

Timely primary-care follow-up has been associated with fewer readmissions in a matched Medicaid cohort, while home-health use after skilled-nursing discharge has also been associated with lower readmission risk.[JAMA Network Open primary-care study](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2722571), [SNF-to-home study](https://pmc.ncbi.nlm.nih.gov/articles/PMC5612845/)

Thus the hospital’s action is not a scalar \(q\). It includes inpatient quality, discharge readiness, medication reconciliation, referral, scheduling, post-acute contracting, patient education, and monitoring.

### 2. States: discharge can lead to several competing outcomes

Replace binary readmission with a multi-state process. For patient \(i\),

\[
S_i(t)\in
\{
\text{alive at home},
\text{outpatient care},
\text{ED},
\text{observation},
\text{planned admission},
\text{unplanned admission},
\text{post-acute facility},
\text{hospice},
\text{death}
\}.
\]

Death is a competing event: a patient who dies cannot subsequently be readmitted. A hospital with worse survival can therefore appear to have fewer readmissions. Competing-risk research shows that conventional binary profiling can rank facilities favorably when their competing-event rate is higher.[Li et al., competing-risk analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC9931495/)

CMS’s original hospital-wide methodology itself excludes in-hospital deaths, requires the patient to be alive at discharge, and excludes some conditions with high post-discharge mortality.[CMS hospital-wide methodology](https://www.cms.gov/medicare/quality-initiatives-patient-assessment-instruments/mms/downloads/mmshospital-wideall-conditionreadmissionrate.pdf) That construction is understandable for defining a readmission denominator, but it means the measure is conditional on surviving and entering the observable risk set.

The appropriate outcome is therefore a joint process such as

\[
\Pr(T_R\leq 30,\ T_R<T_D),
\qquad
\Pr(T_D\leq 30),
\]

not a standalone readmission probability.

### 3. Planned readmissions: not every return signals failure

CMS measures exclude **some planned readmissions**. The planned-readmission algorithm uses procedures and diagnoses to distinguish generally planned care from acute or complication-related returns.[CMS HRRP description](https://www.cms.gov/medicare/quality/value-based-programs/hospital-readmissions)

Chart validation found that the claims algorithm had high specificity but limited sensitivity. In the revised version studied, weighted sensitivity was 49.8%, specificity 96.5%, and positive predictive value 58.7%; performance was particularly weak for some common cardiac procedures.[Horwitz et al., algorithm development and validation](https://pmc.ncbi.nlm.nih.gov/articles/PMC5459369/)

Consequently, latent clinical status \(U_i\in\{\text{planned},\text{unplanned}\}\) differs from algorithmic classification \(\widehat U_i\). The measured outcome is

\[
Y_i^{CMS}
=
\mathbf 1
\{
\text{inpatient claim within 30 days}
\}
\mathbf 1
\{
\widehat U_i=\text{unplanned}
\},
\]

not “avoidable failure caused by hospital quality.”

### 4. Observation window: the quality signal is not constant for 30 days

The baseline assumes a common causal link from index quality to every return during days 1–30. Evidence does not support that restriction.

Hospital-level quality variation in readmission risk appears strongest immediately after discharge and declines rapidly, reaching a low point around seven days in one multistate analysis.[Health Affairs study](https://pubmed.ncbi.nlm.nih.gov/27702961/) Chart-adjudicated research across ten academic centers found that readmissions within seven days had roughly twice the odds of being preventable as later 8–30-day returns.[Primary multicenter study](https://pmc.ncbi.nlm.nih.gov/articles/PMC6247894/)

Let

\[
r_i(t)
=
r^{H}_i(t;q_h)
+
r^{P}_i(t;a_i)
+
r^{D}_i(t;x_i),
\]

where \(r^H\) is attributable to index-hospital care, \(r^P\) to post-discharge care and access, and \(r^D\) to disease progression. The relative weight of \(r^H\) need not remain constant through day 30.

A single 30-day coefficient therefore averages across clinically different hazards. The study should estimate event-time effects and test for displacement to day 31 or later.

### 5. Measurement: inpatient readmission is only one acute-care classification

Returning patients may be treated in an emergency department, placed under observation, or formally admitted. Those classifications affect the CMS numerator even when patient need is similar.

One national study found that observation use increased while readmissions fell but did not find a hospital-level relationship indicating that observation substitution explained the decline.[Zuckerman et al., NEJM](https://www.nejm.org/doi/full/10.1056/NEJMsa1513024)

A later study that included observation stays as both index and return events found that doing so more than halved the apparent decline associated with HRRP and eliminated its estimated association with lower readmissions in the study’s difference-in-differences specification.[Wadhera et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9672971/)

These findings are contradictory rather than interchangeable. They establish that observation substitution is a live measurement mechanism whose importance depends on design and definition; they do not establish that all HRRP reductions are gaming.

CMS now also reports “hospital return days” or excess-days-in-acute-care measures that incorporate inpatient, observation, and emergency-department use, implicitly recognizing that binary inpatient readmission omits relevant acute returns.[CMS unplanned hospital visits](https://data.cms.gov/provider-data/topics/hospitals/unplanned-hospital-visits)

### 6. Coding and risk adjustment: measured performance depends on documentation

CMS compares predicted with expected unplanned readmissions using claims-based risk adjustment. Current HRRP comparisons also place hospitals into peer groups based on the proportion of patients dually eligible for Medicare and full Medicaid benefits.[CMS Provider Data Catalog](https://data.cms.gov/provider-data/topics/hospitals/linking-quality-to-payment)

Let measured severity be

\[
\widehat x_i=x_i+k_h,
\]

where \(x_i\) is clinical severity and \(k_h\) represents documentation and coding intensity. Risk-standardized performance becomes

\[
\widehat r_h
=
\mathcal M
\left(
Y_i^{CMS},\widehat x_i,\text{service mix}
\right).
\]

Hospitals can improve measured performance through real care, more complete coding, or changes in which patients enter the denominator.

A study of coded severity under HRRP found that the 2011 expansion in allowable secondary diagnosis fields increased coded severity, although the authors did not find a statistically significant effect of an additional coded condition category on penalties.[Primary coding study](https://pmc.ncbi.nlm.nih.gov/articles/PMC7572594/) This is useful negative evidence: coding is a plausible measurement channel, but this study does not show that it explains observed penalty reductions.

Claims adjustment also cannot fully observe frailty, health literacy, housing instability, caregiver availability, medication affordability, or transportation. Research adding social-risk measures found that poverty, disability, housing instability, and neighborhood disadvantage predicted readmission and that additional adjustment substantially reduced—but did not eliminate—penalty differences for safety-net hospitals.[Joynt Maddox et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6407348/)

### 7. Post-acute access and patient heterogeneity alter feasible quality

Patient \(i\)’s post-discharge transition technology should be written as

\[
H_{i,t+1}
=
F
\left(
H_{it},
q_h,
A_i,
Z_i,
C_i,
\varepsilon_i
\right),
\]

where:

- \(A_i\): outpatient and post-acute access;
- \(Z_i\): social and economic constraints;
- \(C_i\): caregiver and self-management capacity;
- \(H_{it}\): disease and functional state.

The same hospital action can therefore have different effects across patients. Patients with unstable housing, limited transportation, weak primary-care access, cognitive impairment, or no caregiver may face higher return risk even under identical inpatient care.

This does not mean social risk should automatically be removed from accountability. It means the welfare and production model must distinguish:

- factors the hospital can reasonably influence;
- factors requiring payment for additional transition resources;
- factors outside the hospital’s feasible action set;
- disparities that should remain visible rather than statistically normalized away.

### 8. Selection: the hospital can change who enters the measure

Let \(a_h(x)\) be index admission, transfer, discharge, or service-line acceptance; let \(d_h(x)\) be discharge destination; and let \(e_h(x)\) denote hospice or other end-of-life transition.

The measured readmission rate is conditional on these choices:

\[
\Pr
\left(
Y_i^{CMS}=1
\mid
a_h=1,\ \text{alive at discharge},\ d_h,\ e_h
\right).
\]

A hospital might alter:

- admission thresholds;
- transfers;
- service mix;
- discharge timing;
- post-acute destination;
- hospice referral;
- willingness to treat high-risk or socially complex patients.

A lower measured readmission rate produced by avoiding high-risk patients is not quality improvement. Nor is a reduction produced by higher mortality.

### 9. Incentives: penalties act on a measured proxy, not directly on welfare

The hospital chooses a vector

\[
\mathbf a_h
=
(q^{in},q^{dis},q^{post},m,z,k,s,\tau),
\]

where:

- \(q^{in}\): inpatient treatment quality;
- \(q^{dis}\): discharge and transition quality;
- \(q^{post}\): post-discharge coordination;
- \(m\): monitoring or surveillance;
- \(z\): inpatient versus observation classification;
- \(k\): coding effort;
- \(s\): patient/service selection;
- \(\tau\): timing of return or discharge.

Hospital profit becomes

\[
\Pi_h
=
P_h(\mathbf a_h)
-C_h(\mathbf a_h)
-\Phi_h\!\left(\widehat r_h(\mathbf a_h)\right).
\]

The penalty raises socially valuable quality only if lowering the measured rate is cheapest through genuine care improvement. If substitution, selection, coding, or timing is cheaper, the comparative static for true quality is ambiguous.

## Revised mechanism model

For each discharged patient, define latent clinical need for acute return \(N_i(t)\), survival \(D_i(t)\), access \(A_i(t)\), and hospital response \(a_h\).

The clinically relevant event process is

\[
\begin{aligned}
\lambda_D(t)&=\lambda_D(H_i,q^{in},q^{dis},A_i),\\
\lambda_U(t)&=\lambda_U(H_i,q^{in},q^{dis},q^{post},A_i),\\
\lambda_P(t)&=\lambda_P(H_i,\text{treatment plan}),\\
J_i(t)&\in\{\text{ED},\text{observation},\text{inpatient}\}.
\end{aligned}
\]

The CMS outcome is generated through a measurement function:

\[
Y_i^{CMS}
=
g\!\left(
T_U,T_P,T_D,J_i,
\widehat U_i,
\widehat x_i,
\text{eligibility and exclusions},
30
\right).
\]

Social welfare should instead evaluate

\[
W
=
\sum_i \omega_i
\left[
V(H_i,\text{survival},\text{time at home})
-
C_i^{care}
-
C_i^{travel/caregiving}
\right]
-
C_h(\mathbf a_h)
-
C_{\text{post-acute}}
-
C_{\text{public}}
\]

and should include:

- mortality and health;
- planned and unplanned acute care;
- ED and observation use;
- time alive and outside institutions;
- patient and caregiver burden;
- hospital and post-acute resource costs;
- access and distribution;
- fiscal transfers separately from real resource costs.

Penalty revenue or reduced Medicare payment is principally a transfer unless it changes real resources, entry, staffing, or care.

## Claim, evidence, and falsifier ledger

| Baseline claim | Evidence-based status | Evidence | What would falsify or further narrow the revised claim? |
|---|---|---|---|
| Some costly hospital actions reduce avoidable returns | **Retain** | CMS methodology and transitional-care studies identify discharge readiness, medication management, communication, and follow-up as actionable margins | Well-powered interventions that change these processes but not early unplanned acute returns or patient health |
| All 30-day all-cause readmissions are quality failures | **Contradicted** | CMS excludes some planned readmissions; chart validation shows imperfect planned/unplanned classification | No plausible repair; abandon the universal statement |
| Lower readmission is monotonically better quality | **Contradicted** | Death competes with readmission; inpatient admission can be replaced by observation or ED care | Joint mortality, acute-care, and home-time measures moving consistently would support a narrower local interpretation |
| The 30-day window has a constant hospital-quality signal | **Contradicted** | Hospital-level signal and adjudicated preventability decline after the first week | Similar hospital-attributable hazard and preventability across days 1–30 in independent chart-linked data |
| Claims risk adjustment fully isolates hospital performance | **Contradicted** | Coding changes, residual social risk, frailty, access, and service-mix differences remain | Clinical-registry adjustment and claims adjustment yielding stable rankings across coding and social-risk regimes |
| HRRP penalizes hospital-wide all-cause readmission | **Contradicted as an institutional claim** | CMS states that HRRP uses six condition/procedure-specific unplanned measures; hospital-wide readmission is in IQR | Only a future CMS rule changing HRRP’s included measures |
| Penalties induce hospital behavior | **Retain, bounded** | National readmission trends changed around policy introduction; hospitals face explicit payment reductions | No differential response by actual marginal penalty exposure after addressing anticipation and concurrent trends |
| Reduced inpatient readmission under HRRP proves true quality improvement | **Abandon** | Observation-inclusive analyses materially change estimated effects; mortality evidence is contested | Requires improvement in clinically adjudicated preventable events, survival, home time, and total acute-care use without selection or coding shifts |
| HRRP necessarily increased mortality | **Not established** | One heart-failure registry study found lower readmission and higher mortality, but it is observational and competing studies/designs differ | Designs with credible counterfactuals, consistent diagnosis definitions, and joint event models |
| Observation substitution explains all reported improvement | **Contradicted** | NEJM study found no hospital-level association; later inclusive analysis found a large role | Effect must be estimated by period, condition, and hospital rather than imposed |
| Lower readmission necessarily raises social welfare | **Abandon** | Welfare also depends on mortality, ED/observation use, access, patient burden, real resource costs, and distribution | Only a complete welfare accounting could restore a conditional claim |
| A single average effect applies to all patients | **Contradicted** | Social risk, functional status, caregiver resources, disease, and post-acute access change readmission production | Stable effects across prespecified clinical and social-risk groups in linked data |

## Research design

### Objective

Distinguish five responses to readmission penalties:

1. true quality improvement;
2. substitution across inpatient, observation, and ED status;
3. patient or service selection;
4. increased surveillance and outpatient management;
5. coding or risk-adjustment responses.

### Design structure

Use Medicare claims linked to:

- clinical registry or EHR severity at index admission;
- ED and observation encounters;
- mortality and hospice;
- post-acute facility and home-health use;
- outpatient visits and medication fills;
- diagnosis-code counts and present-on-admission indicators;
- hospital service lines, transfers, and discharge destinations;
- hospital-specific marginal HRRP penalty exposure.

Estimate an event-study/triple-difference design:

\[
Y_{iht}
=
\alpha_h+\gamma_t+\delta_c
+
\beta
\left(
Target_c
\times
Exposure_h^{pre}
\times
Post_t
\right)
+
X_{iht}'\theta+\varepsilon_{iht}.
\]

Here:

- \(Target_c\) identifies HRRP-targeted conditions;
- \(Exposure_h^{pre}\) is fixed using pre-policy information and measures the hospital’s predicted marginal penalty exposure;
- \(Post_t\) distinguishes announcement, implementation, and later penalty-intensity periods;
- hospital, time, and condition effects absorb common differences.

This is not automatically causal. It requires parallel pretrends conditional on exposure, no simultaneous exposure-correlated reform, and explicit treatment of policy anticipation. The exposure interaction should not be redefined after seeing results.

### Pre-specified outcome families

**Clinical outcomes**

- 7-, 30-, and 90-day mortality;
- clinically adjudicated preventable readmission where available;
- complications and functional outcomes;
- days alive and at home.

**Total acute-care use**

- inpatient readmission;
- observation stays;
- ED visits;
- CMS-style excess days in acute care;
- day-specific return hazards through at least day 60.

**Selection and disposition**

- index admission volume and severity;
- transfer rates;
- service-line exits;
- discharge timing;
- skilled-nursing, home-health, and hospice discharge;
- proportion surviving to discharge and entering the readmission denominator.

**Surveillance and access**

- outpatient contact within 7 days;
- specialist and primary-care follow-up;
- medication fills;
- home-health visits;
- diagnostic testing.

**Coding**

- diagnosis fields and comorbidity counts;
- divergence between claims severity and registry severity;
- changes in predicted risk holding clinical variables fixed;
- hospital ranking under frozen versus contemporaneous coding rules.

### Mechanism signatures

| Observed pattern | Interpretation |
|---|---|
| Inpatient readmission falls; mortality does not rise; total acute-care days fall; home time rises; clinical processes improve | Consistent with true quality improvement |
| Inpatient readmission falls; observation or ED use rises one-for-one; total acute-care use unchanged | Status substitution |
| Inpatient readmission falls; day-31-to-60 admissions rise | Timing displacement |
| Readmission falls; index volume or clinical severity falls; transfers or hospice rise | Selection or denominator change |
| Risk-standardized readmission falls; raw events and registry-adjusted events do not; coded severity rises | Coding response |
| Early outpatient contact rises and all acute returns fall | Effective transition management |
| Outpatient surveillance rises together with detected illness and readmission | Surveillance/detection response |
| Readmission falls while mortality rises | Ambiguous or harmful substitution; not quality improvement |
| Average readmission falls but high-risk or socially constrained groups worsen | Distributional failure |

### Stronger measurement strategy

Estimate a multistate competing-risk model rather than a binary logit:

\[
\text{home}
\rightarrow
\{
\text{ED},
\text{observation},
\text{planned admission},
\text{unplanned admission},
\text{death}
\}.
\]

Report both:

- cause-specific hazards;
- cumulative incidence and time alive outside acute or institutional care.

Freeze at least one historical CMS algorithm and risk model across the full study period, then compare it with contemporaneous coding. This separates actual event changes from changes in classification rules and documentation.

## Final disposition of the proposed claims

- **Retain:** hospitals can undertake costly actions that reduce some preventable post-discharge acute events.
- **Narrow:** early, unplanned readmission can be one signal of transition quality for defined populations and conditions.
- **Contradict:** 30-day all-cause readmission is a direct monotone hospital-quality measure.
- **Contradict:** HRRP is a penalty on the hospital-wide all-cause measure.
- **Abandon:** a lower measured readmission rate by itself proves higher \(q\).
- **Abandon:** HRRP necessarily raises social welfare.
- **Replace with:** HRRP changes a vector of hospital care, classification, coding, selection, and coordination choices; its welfare effect must be inferred from joint health, utilization, access, cost, and distributional outcomes.

## Stop reason and reopening rule

I stop here because every mechanism named in the request now changes a specific part of the economic model and has direct support from either CMS documentation or primary research:

- planned versus unplanned classification;
- death as a competing event;
- the 30-day window;
- observation and ED substitution;
- claims coding and risk adjustment;
- post-acute and outpatient access;
- selection and denominator construction;
- patient heterogeneity and social risk;
- mortality, acute-care use, and welfare.

Additional searching is now unlikely to change the decision: the scalar-\(q\), monotone-readmission model should be abandoned and replaced by a multiaction, multistate measurement model.

Reopen the frontier search if CMS publishes materially revised FY2026/2027 final measure specifications, if a new study links clinical severity, inpatient/observation/ED status, coding, hospice, mortality, and post-acute care in one causal design, or if the proposed study identifies a specific condition and policy discontinuity that changes the relevant clinical and institutional boundaries.
