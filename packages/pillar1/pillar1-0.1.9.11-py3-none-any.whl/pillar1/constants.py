STARCODER_BETA = """

Given this `claims` table description:
Here is the describe of the table
Given this `claims` table description:

col_name,data_type,comment
source,string, The insurance company that submitted the claim, only used when insurance provider information is needed. example: FEP, PRIME, BCBS, NASCO, FACETS
NetworkID,int,
DiagCode,string, example (S31102, J09, M12021, G5760, S0282XA, S52044, S72141R, S83111)
DiagDesc,string, various deseases such as diabetes or heart failure, etc will be documented here in sentence form. use this field for questions about diagnosis details and 
names, use this column to identify diabetic patients
IncurredDate, date - the date when a visit took place, such a date of a visit to a doctor's office, Emrgency Room or Nursing Home
SubmittedDate, date - the date when the claim was submitted by the provider
PaidDate, date, the date when the claim was paid
SubmittedAmount,int,
PaidAmount,int,
ClaimStatus,string,
ServicingProviderNPI,bigint,
ServicingProviderName,string, the name of the attending physician, also known as 'service provider' 
BillingProviderNPI,bigint,
BillingProviderName,string,
PlaceofService,string, used for where the patient was treated example: Emergency Room, Others, Nursing Facilty, Inpatient Hospitl, Outpatient Hospital, Emergency Room, 
OfficeVisit, Outpatient Hospital, Nursing Facilty
DrugName,string, The prescribed drug, this is a drugs pharmaceutical name, not the type of drugs used during analytics 
DrugClass,string, The type of drug prescribed, this is the preferred field to use when identifying types of drugs 
GPI,bigint, 
NDC,string,
DaysSupplied,int, the number of days the drug was supplied
LengthOfStay,int, the number of days the patient was admitted
PatientFirstName,string, 
PatientLastName,string,
PatientGender,string,
PatientDateOfBirth,date, use this today's age minus this column for age related questions
PatientAddress,string,
PatientState,string, the full name of the patient state of residence
PatientZIP,int, the patient zip code
PatientID,string.

Here is the top 10 rows 
Source	NetworkID	DiagCode	DiagDesc	CPTDesc	IncurredDate	SubmittedDate	PaidDate	SubmittedAmount	PaidAmount	ClaimStatus	ServicingProviderNPI	
ServicingProviderName	BillingProviderNPI	BillingProviderName	PlaceofService	DrugName	DrugClass	GPI	NDC	DaysSupplied	LengthOfStay	PatientFirstName	
PatientLastName	PatientGender	PatientDateOfBirth	PatientAddress	PatientState	PatientZIP	PatientID
BCBS	23879	S31102	Unsp open wound of abd wall, epigst rgn w/o penet perit cav	Procedures	10/20/19	6/15/20	5/17/21	3908	3633	Pending	2318839638	Dr. Pam Borer	
5524565637	Dr. John Cooling	Emergency Room	GOLD CAVIAR COLLAGEN SERUM	N/A	3.74334E+12	76214-001	8	12	Rice	Gencke	Male	6/19/50	92084 Shopko Street	Illinois	
60674	587-97-0371
FACETS	44429	J09	Influenza due to certain identified influenza viruses	Radiology	8/7/19	1/25/20	6/16/21	275	3779	Denied	1643377991	Dr. Todd Payne	1983297468	Dr. 
Todd Payne	Others	TRITICUM AESTIVUM POLLEN	ACE inhibitor	4.16543E+13	0268-1522	3	15	Bernadine	Danniel	Female	1/27/84	9583 Donald Road	Virginia	23213	
502-99-2905
BCBS	75930	M12021	Chronic postrheumatic arthropathy [Jaccoud], right elbow	N/A	5/7/19	4/5/20	4/20/21	8840	48	Denied	2920362625	Dr. Pam Borer	9078445202	Dr. 
Madhusudan Gupta	Nursing Facilty	DG HEALTH ANTI ITCH	N/A	8.23877E+13	55910-305	2	6	Boone	Welberry	Male	7/27/99	90627 Leroy Street	Oklahoma	73173	274-94-6544
FACETS	3370	G5760	Lesion of plantar nerve, unspecified lower limb	Anesthesia	7/13/19	9/9/20	11/11/21	7803	4443	Pending	5346329671	Dr. Stephen Anckle	
9466357950	Dr. John Cooling	Inpatient Hospitl	Lyrica	Anticoagulant	2.38386E+13	0071-1019	4	10	Koralle	Benninger	Female	11/15/83	592 Northridge Terrace	
California	95113	556-99-6009
BCBS	74437	S0282XA	Fracture of oth skull and facial bones, left side, init	Procedures	2/5/19	4/29/20	1/28/22	8310	617	Pending	4248662264	Dr. Alice Guzman	
8694500848	Dr. Madhusudan Gupta	Outpatient Hospital	Supersmile	ACE inhibitor	9.57039E+13	53567-0706	6	15	Isidora	Weeden	Female	9/3/17	19065 Shoshone Parkway	
Florida	34108	514-46-8649
FEP	46161	S52044	Nondisplaced fracture of coronoid process of right ulna	Evaluation	2/24/19	12/26/20	4/17/21	3123	3718	Pending	9287425101	Dr. Stephen Anckle	
3570146739	Dr. Stephen Anckle	Emergency Room	CHAMOMILLA	Beta blocker	9.31074E+13	60512-1013	7	12	Aubrey	Etock	Female	11/5/78	4 Sauthoff Pass	Kansas	67205	
695-34-3621
FACETS	45965	S72141R	Displ intertroch fx r femr, 7thR	Services	10/2/19	6/9/20	1/1/22	2368	3922	Denied	4348973639	Dr. Stephen Anckle	4732441281	Dr. John 
Cooling	OfficeVisit	Ibuprofen	Long acting insulins	5.04969E+11	52125-674	5	4	Jerrilyn	Dimitriades	Female	3/16/55	37 Dorton Parkway	Ohio	45403	686-16-5067
FEP	81041	S83111	Anterior subluxation of proximal end of tibia, right knee	N/A	12/14/19	7/10/20	10/30/21	7622	3155	Denied	4247116742	Dr. Madhusudan Gupta	
9277033298	Dr. John Cooling	Outpatient Hospital	Crinone	Sulfonylurea	9.3739E+13	52544-283	10	1	Shel	Stolberg	Female	12/25/68	82026 Mockingbird Pass	
Massachusetts	2119	793-69-0684
FEP	55823	M25839	Other specified joint disorders, unspecified wrist	Radiology	12/7/19	7/7/20	9/24/21	4981	308	Pending	9904073803	Dr. Madhusudan Gupta	5718432993	
Dr. Pam Borer	Outpatient Hospital	Micro-K Extencaps	Beta blocker	2.94649E+13	64011-010	2	14	Rosella	Stearndale	Female	7/7/57	04 Union Crossing	Florida	33028	
864-54-4714
FEP	30373	S55812	Laceration of other blood vessels at forearm level, left arm	Medicine	12/9/19	12/15/20	8/4/21	5773	4286	Paid	2273445390	Dr. Stephen 
Anckle	432849957	Dr. Stephen Anckle	Nursing Facilty	Minitran	Corticosteroid	1.30794E+13	29336-302	5	15	Christalle	Scotson	Female	12/14/82	07 Armistice Place	
Illinois	60351	321-71-5203

For state related queries use the PatientState column, not state

date fields and should be searched as date columns i.e. Year(PaidDate), Month(SubmittedDate), Year(IncurredDate) etc

All date fields should be treated as dates not strings

When completing the code request use the describe listed above and the examples following the describe, do not make up column names and do not place additional conditions. 

Do not include selection clauses which are not explicitly asked for

For all = comparisons use ILIKE instead of = . not LIKE but ILIKE

All string comparisons are done in a case insensitive manner

The SQL statement to answer the question  

use DiagDesc for patient condition queries

"""

APPEND = " Considering every selection where clause criteria without missing any, Columns in the select queries will be given appropriate names, always comparing strings with " \
         "ILIKE (in case insensitive mode),  ILIKE will be used in string where clauses, where conditions which are not asked for explicitly will not be included, " \
         "correctnes is of highest priority, here is the SQL, ```sql"
