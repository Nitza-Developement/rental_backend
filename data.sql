SET session_replication_role = replica;

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6
-- Dumped by pg_dump version 15.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: audit_log_entries; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."audit_log_entries" ("instance_id", "id", "payload", "created_at", "ip_address") FROM stdin;
\.


--
-- Data for Name: flow_state; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."flow_state" ("id", "user_id", "auth_code", "code_challenge_method", "code_challenge", "provider_type", "provider_access_token", "provider_refresh_token", "created_at", "updated_at", "authentication_method", "auth_code_issued_at") FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at", "is_anonymous") FROM stdin;
\.


--
-- Data for Name: identities; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."identities" ("provider_id", "user_id", "identity_data", "provider", "last_sign_in_at", "created_at", "updated_at", "id") FROM stdin;
\.


--
-- Data for Name: instances; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."instances" ("id", "uuid", "raw_base_config", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sessions" ("id", "user_id", "created_at", "updated_at", "factor_id", "aal", "not_after", "refreshed_at", "user_agent", "ip", "tag") FROM stdin;
\.


--
-- Data for Name: mfa_amr_claims; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_amr_claims" ("session_id", "created_at", "updated_at", "authentication_method", "id") FROM stdin;
\.


--
-- Data for Name: mfa_factors; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_factors" ("id", "user_id", "friendly_name", "factor_type", "status", "created_at", "updated_at", "secret", "phone", "last_challenged_at", "web_authn_credential", "web_authn_aaguid") FROM stdin;
\.


--
-- Data for Name: mfa_challenges; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."mfa_challenges" ("id", "factor_id", "created_at", "verified_at", "ip_address", "otp_code", "web_authn_session_data") FROM stdin;
\.


--
-- Data for Name: one_time_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."one_time_tokens" ("id", "user_id", "token_type", "token_hash", "relates_to", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."refresh_tokens" ("instance_id", "id", "token", "user_id", "revoked", "created_at", "updated_at", "parent", "session_id") FROM stdin;
\.


--
-- Data for Name: sso_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sso_providers" ("id", "resource_id", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: saml_providers; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."saml_providers" ("id", "sso_provider_id", "entity_id", "metadata_xml", "metadata_url", "attribute_mapping", "created_at", "updated_at", "name_id_format") FROM stdin;
\.


--
-- Data for Name: saml_relay_states; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."saml_relay_states" ("id", "sso_provider_id", "request_id", "for_email", "redirect_to", "created_at", "updated_at", "flow_state_id") FROM stdin;
\.


--
-- Data for Name: sso_domains; Type: TABLE DATA; Schema: auth; Owner: supabase_auth_admin
--

COPY "auth"."sso_domains" ("id", "sso_provider_id", "domain", "created_at", "updated_at") FROM stdin;
\.


--
-- Data for Name: key; Type: TABLE DATA; Schema: pgsodium; Owner: supabase_admin
--

COPY "pgsodium"."key" ("id", "status", "created", "expires", "key_type", "key_id", "key_context", "name", "associated_data", "raw_key", "raw_key_nonce", "parent_key", "comment", "user_data") FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."django_content_type" ("id", "app_label", "model") FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	django_seeding	appliedseeder
7	token_blacklist	blacklistedtoken
8	token_blacklist	outstandingtoken
9	auditlog	logentry
10	rental	user
11	rental	tenant
12	rental	client
13	rental	tenantuser
14	rental	vehicle
15	rental	vehiclepicture
16	rental	vehicleplate
17	rental	contract
18	rental	note
19	rental	rentalplan
20	rental	stageupdate
21	rental	tolldue
22	rental	tracker
23	rental	trackerheartbeatdata
24	rental	card
25	rental	field
26	rental	checkoption
27	rental	form
28	rental	inspection
29	rental	fieldresponse
30	rental	contractformtemplate
31	rental	contractform
32	rental	contractformfield
33	rental	contractformfieldresponse
34	rental	reminder
\.


--
-- Data for Name: rental_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_user" ("id", "password", "last_login", "email", "image", "date_joined", "is_active", "is_staff", "is_superuser", "name") FROM stdin;
1	pbkdf2_sha256$720000$B0UqbzLOOcfBzmUGw50PMr$J0mzO65LJ/vcjT2cOZgIFzEqooUqVGDE+761pXpM3gQ=	\N	admin@admin.com		2024-11-03 00:57:56.79005+00	t	t	t	Admin
2	pbkdf2_sha256$720000$BxY4no1zP9v1rklnUyyg79$x9GapVM9oc0lON9IAJOPQfe2NguOefF92TI3WWaCHdc=	\N	test-admin@admin.com		2024-11-03 00:58:00.199079+00	t	t	t	Admin-Test
3	pbkdf2_sha256$720000$6QW72u08wra3UPZ61tTxU0$an6i8hKa66GfRjGjSoiChX8Pr8mXMP16aNgDSe/ysYg=	2024-11-03 23:19:42.425083+00	vladimir.rdguez@gmail.com		2024-11-03 01:02:21.30949+00	t	t	t	Vladímir
4	pbkdf2_sha256$720000$0QyZwWN8C0RWlx5dU3QH7R$fkQMb8wXePcybt+DC493ga6EcmiFFeyHP0Fn4Op2oCs=	\N	fc0510507@gmail.com		2024-11-15 19:12:04.740959+00	t	f	f	Frank Carlos
5	pbkdf2_sha256$720000$qtnwgwtje8s3M5MtKDdeaV$eB74ezpWbXKxf4q0Uw6ghZhSrSaMyfsCPsxGO6r/ftk=	\N	raulodev@gmail.com		2024-11-16 02:02:37.96817+00	t	t	t	Raúl
\.


--
-- Data for Name: auditlog_logentry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."auditlog_logentry" ("id", "object_pk", "object_id", "object_repr", "action", "changes", "timestamp", "actor_id", "content_type_id", "remote_addr", "additional_data", "serialized_data", "cid", "changes_text") FROM stdin;
1	1	1	Admin	0	{"id": ["None", "1"], "name": ["None", "Admin"], "email": ["None", "admin@admin.com"], "image": ["None", ""], "notes": ["None", "rental.Note.None"], "is_staff": ["None", "True"], "password": ["None", ""], "is_active": ["None", "True"], "date_joined": ["None", "2024-11-03 00:57:54.697583"], "tenantUsers": ["None", "rental.TenantUser.None"], "is_superuser": ["None", "True"]}	2024-11-03 00:57:55.220786+00	\N	10	\N	\N	\N	\N	
2	1	1	Admin	1	{"password": ["", "pbkdf2_sha256$720000$B0UqbzLOOcfBzmUGw50PMr$J0mzO65LJ/vcjT2cOZgIFzEqooUqVGDE+761pXpM3gQ="]}	2024-11-03 00:57:56.613952+00	\N	10	\N	\N	\N	\N	
3	1	1	1	0	{"id": ["None", "1"], "role": ["None", "Admin"], "user": ["None", "1"], "tenant": ["None", "2"], "is_default": ["None", "True"], "inspections": ["None", "rental.Inspection.None"], "my_reminders": ["None", "rental.Reminder.None"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-03 00:57:57.535286+00	\N	13	\N	\N	\N	\N	
4	2	2	Admin-Test	0	{"id": ["None", "2"], "name": ["None", "Admin-Test"], "email": ["None", "test-admin@admin.com"], "image": ["None", ""], "notes": ["None", "rental.Note.None"], "is_staff": ["None", "True"], "password": ["None", ""], "is_active": ["None", "True"], "date_joined": ["None", "2024-11-03 00:57:58.297747"], "tenantUsers": ["None", "rental.TenantUser.None"], "is_superuser": ["None", "True"]}	2024-11-03 00:57:58.638304+00	\N	10	\N	\N	\N	\N	
5	2	2	Admin-Test	1	{"password": ["", "pbkdf2_sha256$720000$BxY4no1zP9v1rklnUyyg79$x9GapVM9oc0lON9IAJOPQfe2NguOefF92TI3WWaCHdc="]}	2024-11-03 00:58:00.025517+00	\N	10	\N	\N	\N	\N	
6	2	2	2	0	{"id": ["None", "2"], "role": ["None", "Admin"], "user": ["None", "2"], "tenant": ["None", "1"], "is_default": ["None", "True"], "inspections": ["None", "rental.Inspection.None"], "my_reminders": ["None", "rental.Reminder.None"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-03 00:58:00.723866+00	\N	13	\N	\N	\N	\N	
7	3	3		0	{"id": ["None", "3"], "name": ["None", ""], "email": ["None", "vladimir.rdguez@gmail.com"], "image": ["None", ""], "notes": ["None", "rental.Note.None"], "is_staff": ["None", "False"], "password": ["None", "pbkdf2_sha256$720000$6QW72u08wra3UPZ61tTxU0$an6i8hKa66GfRjGjSoiChX8Pr8mXMP16aNgDSe/ysYg="], "is_active": ["None", "True"], "date_joined": ["None", "2024-11-03 01:00:07.975544"], "tenantUsers": ["None", "rental.TenantUser.None"], "is_superuser": ["None", "False"]}	2024-11-03 01:00:08.420157+00	\N	10	\N	\N	\N	\N	
8	3	3		1	{"is_staff": ["False", "True"], "is_superuser": ["False", "True"]}	2024-11-03 01:00:08.845482+00	\N	10	\N	\N	\N	\N	
9	3	3		1	{"last_login": ["None", "2024-11-03 01:00:46.859691"]}	2024-11-03 01:00:47.220296+00	\N	10	127.0.0.1	\N	\N	\N	
10	3	3	3	0	{"id": ["None", "3"], "role": ["None", "Admin"], "user": ["None", "3"], "tenant": ["None", "1"], "is_default": ["None", "False"], "inspections": ["None", "rental.Inspection.None"], "my_reminders": ["None", "rental.Reminder.None"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-03 01:01:21.896879+00	3	13	127.0.0.1	\N	\N	\N	
11	3	3	Vladímir	1	{"name": ["", "Vladímir"], "last_login": ["2024-11-03 01:00:46.859691", "2024-11-03 01:00:46"]}	2024-11-03 01:02:21.126762+00	3	10	127.0.0.1	\N	\N	\N	
12	4	4	4	0	{"id": ["None", "4"], "role": ["None", "Admin"], "user": ["None", "3"], "tenant": ["None", "2"], "is_default": ["None", "True"], "inspections": ["None", "rental.Inspection.None"], "my_reminders": ["None", "rental.Reminder.None"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-03 01:03:03.610406+00	3	13	127.0.0.1	\N	\N	\N	
13	3	3	Vladímir	1	{"last_login": ["2024-11-03 01:00:46", "2024-11-03 18:26:57.160315"]}	2024-11-03 18:26:57.282989+00	\N	10	127.0.0.1	\N	\N	\N	
14	3	3	Vladímir	1	{"last_login": ["2024-11-03 18:26:57.160315", "2024-11-03 23:19:42.425083"]}	2024-11-03 23:19:42.557076+00	\N	10	94.140.11.4	\N	\N	\N	
15	1	1	1G1AF1F57A7190000 | testVehicle | Trailer	0	{"id": ["None", "1"], "vin": ["None", "1G1AF1F57A7190000"], "make": ["None", "BigTex"], "trim": ["None", "null"], "type": ["None", "Trailer"], "year": ["None", "2023"], "model": ["None", "Flatbed"], "plates": ["None", "rental.VehiclePlate.None"], "status": ["None", "Available"], "tenant": ["None", "2"], "nickname": ["None", "testVehicle"], "odometer": ["None", "0"], "contracts": ["None", "rental.Contract.None"], "reminders": ["None", "rental.Reminder.None"], "is_deleted": ["None", "False"], "inspections": ["None", "rental.Inspection.None"], "spare_tires": ["None", "2"], "vehicle_pictures": ["None", "rental.VehiclePicture.None"]}	2024-11-05 15:30:55.473436+00	3	14	\N	\N	\N	\N	
16	1	1	4232rewr324	0	{"id": ["None", "1"], "plate": ["None", "4232rewr324"], "vehicle": ["None", "1"], "is_active": ["None", "True"], "toll_dues": ["None", "rental.TollDue.None"], "assign_date": ["None", "2024-11-05 15:30:55.552304"]}	2024-11-05 15:30:55.687518+00	3	16	\N	\N	\N	\N	
17	1	1	1G1AF1F57A7190000 | testVehicle | Trailer	1	{"spare_tires": ["2", "1"]}	2024-11-05 16:13:31.617092+00	3	14	\N	\N	\N	\N	
18	1	1	Previo a la renta	0	{"id": ["None", "1"], "form": ["None", "1"], "tenant": ["None", "2"], "vehicle": ["None", "1"], "created_at": ["None", "2024-11-06 21:26:30.726011"], "tenantUser": ["None", "4"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-06 21:26:30.849219+00	\N	28	94.140.11.134	\N	\N	\N	
19	1	1	Pepe | ppe@gmail.cu | 3058336104	0	{"id": ["None", "1"], "name": ["None", "Pepe"], "email": ["None", "ppe@gmail.cu"], "tenant": ["None", "2"], "contracts": ["None", "rental.Contract.None"], "reminders": ["None", "rental.Reminder.None"], "phone_number": ["None", "3058336104"]}	2024-11-07 23:36:16.027303+00	3	12	152.207.211.251	\N	\N	\N	
20	1	1	Test-Tenant | Pepe | ppe@gmail.cu | 3058336104 | 1G1AF1F57A7190000 | testVehicle | Trailer	0	{"id": ["None", "1"], "notes": ["None", "rental.Note.None"], "client": ["None", "1"], "tenant": ["None", "2"], "vehicle": ["None", "1"], "reminders": ["None", "rental.Reminder.None"], "toll_dues": ["None", "rental.TollDue.None"], "rental_plan": ["None", "3"], "creation_date": ["None", "2024-11-07 23:37:33.169376"], "stages_updates": ["None", "rental.StageUpdate.None"]}	2024-11-07 23:37:33.304364+00	3	17	152.207.211.251	\N	\N	\N	
21	1	1	Pending | 2024-11-07 23:37:33.372262+00:00 | Test-Tenant | Pepe | ppe@gmail.cu | 3058336104 | 1G1AF1F57A7190000 | testVehicle | Trailer	0	{"id": ["None", "1"], "date": ["None", "2024-11-07 23:37:33.372262"], "stage": ["None", "Pending"], "contract": ["None", "1"]}	2024-11-07 23:37:33.505894+00	3	20	152.207.211.251	\N	\N	\N	
22	2	2	Active | 2024-11-07 23:39:54.354742+00:00 | Test-Tenant | Pepe | ppe@gmail.cu | 3058336104 | 1G1AF1F57A7190000 | testVehicle | Trailer	0	{"id": ["None", "2"], "date": ["None", "2024-11-07 23:39:54.354742"], "stage": ["None", "Active"], "comments": ["None", "Ya quedó firmado"], "contract": ["None", "1"]}	2024-11-07 23:39:54.601477+00	3	20	152.207.211.251	\N	\N	\N	
23	4	4	-	0	{"id": ["None", "4"], "name": ["None", "-"], "email": ["None", "fc0510507@gmail.com"], "image": ["None", ""], "notes": ["None", "rental.Note.None"], "is_staff": ["None", "False"], "password": ["None", "pbkdf2_sha256$720000$ri7dj48KgIkQv83xbRmQdO$kI8nLAAX86g7yyihW8UG6TOpsOwC0fEc4uUsDLXR37M="], "is_active": ["None", "True"], "date_joined": ["None", "2024-11-13 20:19:46.210676"], "tenantUsers": ["None", "rental.TenantUser.None"], "is_superuser": ["None", "False"]}	2024-11-13 20:19:46.364245+00	3	10	181.214.151.29	\N	\N	\N	
24	5	5	5	0	{"id": ["None", "5"], "role": ["None", "Admin"], "user": ["None", "4"], "tenant": ["None", "2"], "is_default": ["None", "True"], "inspections": ["None", "rental.Inspection.None"], "my_reminders": ["None", "rental.Reminder.None"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-13 20:19:46.891468+00	3	13	181.214.151.29	\N	\N	\N	
25	4	4	Frank Carlos	1	{"name": ["-", "Frank Carlos"]}	2024-11-13 20:24:56.593764+00	3	10	181.214.151.29	\N	\N	\N	
26	4	4	Frank Carlos	1	{"password": ["pbkdf2_sha256$720000$ri7dj48KgIkQv83xbRmQdO$kI8nLAAX86g7yyihW8UG6TOpsOwC0fEc4uUsDLXR37M=", "pbkdf2_sha256$720000$0QyZwWN8C0RWlx5dU3QH7R$fkQMb8wXePcybt+DC493ga6EcmiFFeyHP0Fn4Op2oCs="]}	2024-11-15 19:12:04.657068+00	\N	10	\N	\N	\N	\N	
27	5	5	Raúl	0	{"id": ["None", "5"], "name": ["None", "Raúl"], "email": ["None", "raulodev@gmail.com"], "image": ["None", ""], "notes": ["None", "rental.Note.None"], "is_staff": ["None", "True"], "password": ["None", "qJNSvLwnRFg9QfzEtaeyUT"], "is_active": ["None", "True"], "date_joined": ["None", "2024-11-15 19:41:56.309517"], "tenantUsers": ["None", "rental.TenantUser.None"], "is_superuser": ["None", "True"]}	2024-11-15 19:41:56.375949+00	3	10	2.59.157.57	\N	\N	\N	
28	6	6	6	0	{"id": ["None", "6"], "role": ["None", "Admin"], "user": ["None", "5"], "tenant": ["None", "1"], "is_default": ["None", "False"], "inspections": ["None", "rental.Inspection.None"], "my_reminders": ["None", "rental.Reminder.None"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-15 19:43:09.62746+00	3	13	2.59.157.57	\N	\N	\N	
29	7	7	7	0	{"id": ["None", "7"], "role": ["None", "Admin"], "user": ["None", "5"], "tenant": ["None", "2"], "is_default": ["None", "True"], "inspections": ["None", "rental.Inspection.None"], "my_reminders": ["None", "rental.Reminder.None"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-15 19:43:23.412043+00	3	13	2.59.157.57	\N	\N	\N	
30	5	5	Raúl	1	{"password": ["qJNSvLwnRFg9QfzEtaeyUT", "pbkdf2_sha256$720000$qtnwgwtje8s3M5MtKDdeaV$eB74ezpWbXKxf4q0Uw6ghZhSrSaMyfsCPsxGO6r/ftk="]}	2024-11-16 02:02:37.903979+00	\N	10	\N	\N	\N	\N	
31	2	2	Formulario	0	{"id": ["None", "2"], "form": ["None", "2"], "tenant": ["None", "2"], "vehicle": ["None", "1"], "created_at": ["None", "2024-11-17 00:50:05.186526"], "tenantUser": ["None", "4"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-17 00:50:05.314776+00	3	28	152.206.141.147	\N	\N	\N	
32	3	3	Simple	0	{"id": ["None", "3"], "form": ["None", "4"], "tenant": ["None", "2"], "vehicle": ["None", "1"], "created_at": ["None", "2024-11-17 03:31:21.926268"], "tenantUser": ["None", "7"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-17 03:31:21.997718+00	\N	28	45.87.214.82	\N	\N	\N	
33	4	4	Formulario	0	{"id": ["None", "4"], "form": ["None", "2"], "tenant": ["None", "2"], "vehicle": ["None", "1"], "created_at": ["None", "2024-11-18 16:48:51.566507"], "tenantUser": ["None", "4"], "field_responses": ["None", "rental.FieldResponse.None"]}	2024-11-18 16:48:51.635579+00	\N	28	152.207.211.106	\N	\N	\N	
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."auth_group" ("id", "name") FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."auth_permission" ("id", "name", "content_type_id", "codename") FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add applied seeder	6	add_appliedseeder
22	Can change applied seeder	6	change_appliedseeder
23	Can delete applied seeder	6	delete_appliedseeder
24	Can view applied seeder	6	view_appliedseeder
25	Can add blacklisted token	7	add_blacklistedtoken
26	Can change blacklisted token	7	change_blacklistedtoken
27	Can delete blacklisted token	7	delete_blacklistedtoken
28	Can view blacklisted token	7	view_blacklistedtoken
29	Can add outstanding token	8	add_outstandingtoken
30	Can change outstanding token	8	change_outstandingtoken
31	Can delete outstanding token	8	delete_outstandingtoken
32	Can view outstanding token	8	view_outstandingtoken
33	Can add log entry	9	add_logentry
34	Can change log entry	9	change_logentry
35	Can delete log entry	9	delete_logentry
36	Can view log entry	9	view_logentry
37	Can add User	10	add_user
38	Can change User	10	change_user
39	Can delete User	10	delete_user
40	Can view User	10	view_user
41	Can add Tenant	11	add_tenant
42	Can change Tenant	11	change_tenant
43	Can delete Tenant	11	delete_tenant
44	Can view Tenant	11	view_tenant
45	Can add Client	12	add_client
46	Can change Client	12	change_client
47	Can delete Client	12	delete_client
48	Can view Client	12	view_client
49	Can add Tenant User	13	add_tenantuser
50	Can change Tenant User	13	change_tenantuser
51	Can delete Tenant User	13	delete_tenantuser
52	Can view Tenant User	13	view_tenantuser
53	Can add Vehicle	14	add_vehicle
54	Can change Vehicle	14	change_vehicle
55	Can delete Vehicle	14	delete_vehicle
56	Can view Vehicle	14	view_vehicle
57	Can add vehicle picture	15	add_vehiclepicture
58	Can change vehicle picture	15	change_vehiclepicture
59	Can delete vehicle picture	15	delete_vehiclepicture
60	Can view vehicle picture	15	view_vehiclepicture
61	Can add vehicle plate	16	add_vehicleplate
62	Can change vehicle plate	16	change_vehicleplate
63	Can delete vehicle plate	16	delete_vehicleplate
64	Can view vehicle plate	16	view_vehicleplate
65	Can add Contract	17	add_contract
66	Can change Contract	17	change_contract
67	Can delete Contract	17	delete_contract
68	Can view Contract	17	view_contract
69	Can add Note	18	add_note
70	Can change Note	18	change_note
71	Can delete Note	18	delete_note
72	Can view Note	18	view_note
73	Can add Rental Plan	19	add_rentalplan
74	Can change Rental Plan	19	change_rentalplan
75	Can delete Rental Plan	19	delete_rentalplan
76	Can view Rental Plan	19	view_rentalplan
77	Can add Stage	20	add_stageupdate
78	Can change Stage	20	change_stageupdate
79	Can delete Stage	20	delete_stageupdate
80	Can view Stage	20	view_stageupdate
81	Can add TollDue	21	add_tolldue
82	Can change TollDue	21	change_tolldue
83	Can delete TollDue	21	delete_tolldue
84	Can view TollDue	21	view_tolldue
85	Can add Tracker	22	add_tracker
86	Can change Tracker	22	change_tracker
87	Can delete Tracker	22	delete_tracker
88	Can view Tracker	22	view_tracker
89	Can add Tracker Heart Beat Data	23	add_trackerheartbeatdata
90	Can change Tracker Heart Beat Data	23	change_trackerheartbeatdata
91	Can delete Tracker Heart Beat Data	23	delete_trackerheartbeatdata
92	Can view Tracker Heart Beat Data	23	view_trackerheartbeatdata
93	Can add card	24	add_card
94	Can change card	24	change_card
95	Can delete card	24	delete_card
96	Can view card	24	view_card
97	Can add field	25	add_field
98	Can change field	25	change_field
99	Can delete field	25	delete_field
100	Can view field	25	view_field
101	Can add check option	26	add_checkoption
102	Can change check option	26	change_checkoption
103	Can delete check option	26	delete_checkoption
104	Can view check option	26	view_checkoption
105	Can add form	27	add_form
106	Can change form	27	change_form
107	Can delete form	27	delete_form
108	Can view form	27	view_form
109	Can add inspection	28	add_inspection
110	Can change inspection	28	change_inspection
111	Can delete inspection	28	delete_inspection
112	Can view inspection	28	view_inspection
113	Can add field response	29	add_fieldresponse
114	Can change field response	29	change_fieldresponse
115	Can delete field response	29	delete_fieldresponse
116	Can view field response	29	view_fieldresponse
117	Can add contract form template	30	add_contractformtemplate
118	Can change contract form template	30	change_contractformtemplate
119	Can delete contract form template	30	delete_contractformtemplate
120	Can view contract form template	30	view_contractformtemplate
121	Can add contract form	31	add_contractform
122	Can change contract form	31	change_contractform
123	Can delete contract form	31	delete_contractform
124	Can view contract form	31	view_contractform
125	Can add contract form field	32	add_contractformfield
126	Can change contract form field	32	change_contractformfield
127	Can delete contract form field	32	delete_contractformfield
128	Can view contract form field	32	view_contractformfield
129	Can add contract form field response	33	add_contractformfieldresponse
130	Can change contract form field response	33	change_contractformfieldresponse
131	Can delete contract form field response	33	delete_contractformfieldresponse
132	Can view contract form field response	33	view_contractformfieldresponse
133	Can add reminder	34	add_reminder
134	Can change reminder	34	change_reminder
135	Can delete reminder	34	delete_reminder
136	Can view reminder	34	view_reminder
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."auth_group_permissions" ("id", "group_id", "permission_id") FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."django_admin_log" ("id", "action_time", "object_id", "object_repr", "action_flag", "change_message", "content_type_id", "user_id") FROM stdin;
1	2024-11-03 01:01:22.082753+00	3	3	1	[{"added": {}}]	13	3
2	2024-11-03 01:02:21.84401+00	3	Vladímir	2	[{"changed": {"fields": ["Name"]}}]	10	3
3	2024-11-03 01:03:03.787613+00	4	4	1	[{"added": {}}]	13	3
4	2024-11-13 20:24:56.858963+00	4	Frank Carlos	2	[{"changed": {"fields": ["Name"]}}]	10	3
5	2024-11-15 19:41:56.584922+00	5	Raúl	1	[{"added": {}}]	10	3
6	2024-11-15 19:43:09.687845+00	6	6	1	[{"added": {}}]	13	3
7	2024-11-15 19:43:23.474232+00	7	7	1	[{"added": {}}]	13	3
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."django_migrations" ("id", "app", "name", "applied") FROM stdin;
1	rental	0001_initial	2024-11-03 00:47:48.61268+00
2	contenttypes	0001_initial	2024-11-03 00:47:49.308555+00
3	admin	0001_initial	2024-11-03 00:47:50.891601+00
4	admin	0002_logentry_remove_auto_add	2024-11-03 00:47:51.082358+00
5	admin	0003_logentry_add_action_flag_choices	2024-11-03 00:47:51.600024+00
6	auditlog	0001_initial	2024-11-03 00:47:53.892038+00
7	auditlog	0002_auto_support_long_primary_keys	2024-11-03 00:47:54.985604+00
8	auditlog	0003_logentry_remote_addr	2024-11-03 00:47:55.694924+00
9	auditlog	0004_logentry_detailed_object_repr	2024-11-03 00:47:56.391543+00
10	auditlog	0005_logentry_additional_data_verbose_name	2024-11-03 00:47:56.751343+00
11	auditlog	0006_object_pk_index	2024-11-03 00:47:57.96354+00
12	auditlog	0007_object_pk_type	2024-11-03 00:47:58.321115+00
13	auditlog	0008_action_index	2024-11-03 00:47:59.194119+00
14	auditlog	0009_alter_logentry_additional_data	2024-11-03 00:47:59.567045+00
15	auditlog	0010_alter_logentry_timestamp	2024-11-03 00:48:00.423191+00
16	auditlog	0011_logentry_serialized_data	2024-11-03 00:48:01.106904+00
17	auditlog	0012_add_logentry_action_access	2024-11-03 00:48:01.469514+00
18	auditlog	0013_alter_logentry_timestamp	2024-11-03 00:48:02.167866+00
19	auditlog	0014_logentry_cid	2024-11-03 00:48:03.836476+00
20	auditlog	0015_alter_logentry_changes	2024-11-03 00:48:04.809305+00
21	contenttypes	0002_remove_content_type_name	2024-11-03 00:48:05.719894+00
22	auth	0001_initial	2024-11-03 00:48:08.595355+00
23	auth	0002_alter_permission_name_max_length	2024-11-03 00:48:09.188745+00
24	auth	0003_alter_user_email_max_length	2024-11-03 00:48:09.539351+00
25	auth	0004_alter_user_username_opts	2024-11-03 00:48:10.05001+00
26	auth	0005_alter_user_last_login_null	2024-11-03 00:48:10.568201+00
27	auth	0006_require_contenttypes_0002	2024-11-03 00:48:11.078853+00
28	auth	0007_alter_validators_add_error_messages	2024-11-03 00:48:11.609274+00
29	auth	0008_alter_user_username_max_length	2024-11-03 00:48:12.127921+00
30	auth	0009_alter_user_last_name_max_length	2024-11-03 00:48:12.648851+00
31	auth	0010_alter_group_name_max_length	2024-11-03 00:48:13.546947+00
32	auth	0011_update_proxy_permissions	2024-11-03 00:48:13.915884+00
33	auth	0012_alter_user_first_name_max_length	2024-11-03 00:48:14.437539+00
34	django_seeding	0001_initial	2024-11-03 00:48:15.653885+00
35	rental	0002_user_is_staff	2024-11-03 00:48:16.354903+00
36	rental	0003_remove_user_is_staff	2024-11-03 00:48:17.043307+00
37	rental	0004_alter_tenantuser_unique_together	2024-11-03 00:48:17.769111+00
38	rental	0005_alter_client_phone_number	2024-11-03 00:48:18.114715+00
39	rental	0006_user_date_joined_user_is_active_user_is_staff	2024-11-03 00:48:19.863364+00
40	rental	0007_alter_customuser_options_and_more	2024-11-03 00:48:24.445341+00
41	rental	0008_customuser_name_alter_customuser_username	2024-11-03 00:48:25.539957+00
42	rental	0009_alter_customuser_name	2024-11-03 00:48:25.912362+00
43	rental	0010_alter_customuser_name	2024-11-03 00:48:26.449027+00
44	rental	0011_alter_customuser_options_and_more	2024-11-03 00:48:27.763721+00
45	rental	0012_alter_client_tenant_alter_tenantuser_tenant	2024-11-03 00:48:28.233313+00
46	rental	0013_tenant_date_joined	2024-11-03 00:48:29.256444+00
47	rental	0014_vehicle_vehiclepicture_vehicleplate	2024-11-03 00:48:31.576844+00
48	rental	0015_vehicle_tenant	2024-11-03 00:48:32.480737+00
49	rental	0016_alter_vehicle_tenant	2024-11-03 00:48:34.157068+00
50	rental	0017_alter_vehiclepicture_id_alter_vehiclepicture_image	2024-11-03 00:48:35.395888+00
51	rental	0018_contract_note_rentalplan_contract_rental_plan_and_more	2024-11-03 00:48:42.022216+00
52	rental	0019_alter_stageupdate_previous_stage	2024-11-03 00:48:43.136295+00
53	rental	0020_alter_stageupdate_options_and_more	2024-11-03 00:48:44.436719+00
54	rental	0021_alter_tracker_options_and_more	2024-11-03 00:48:46.413776+00
55	rental	0022_alter_client_options_alter_contract_options_and_more	2024-11-03 00:48:46.9128+00
56	rental	0023_card_field_checkoption_form_card_form_inspection_and_more	2024-11-03 00:48:53.168164+00
57	rental	0024_alter_field_type_alter_fieldresponse_note	2024-11-03 00:48:53.751093+00
58	rental	0025_alter_tenantuser_unique_together	2024-11-03 00:48:54.844341+00
59	rental	0026_alter_rentalplan_unique_together_rentalplan_tenant_and_more	2024-11-03 00:48:56.939787+00
60	rental	0027_alter_rentalplan_tenant	2024-11-03 00:48:57.193932+00
61	rental	0028_alter_rentalplan_tenant	2024-11-03 00:48:57.78584+00
62	rental	0029_alter_vehicle_type	2024-11-03 00:48:58.341246+00
63	rental	0030_alter_vehicle_type	2024-11-03 00:48:58.888059+00
64	rental	0031_remove_vehicle_model	2024-11-03 00:48:59.7524+00
65	rental	0032_alter_stageupdate_options_vehicle_model	2024-11-03 00:49:00.983154+00
66	rental	0033_vehicle_is_deleted	2024-11-03 00:49:01.960585+00
67	rental	0034_alter_vehicle_status	2024-11-03 00:49:02.345514+00
68	rental	0035_alter_vehicle_type	2024-11-03 00:49:02.903172+00
69	rental	0036_alter_vehicle_make_alter_vehicle_model_and_more	2024-11-03 00:49:04.577444+00
70	rental	0037_alter_vehicle_odometer	2024-11-03 00:49:05.291023+00
71	rental	0038_alter_vehicle_spare_tires	2024-11-03 00:49:06.007793+00
72	rental	0039_alter_form_options_alter_card_form_and_more	2024-11-03 00:49:06.475349+00
73	rental	0040_alter_field_type	2024-11-03 00:49:06.998061+00
74	rental	0041_alter_form_options_checkoption_type	2024-11-03 00:49:08.057865+00
75	rental	0042_alter_inspection_options	2024-11-03 00:49:08.455021+00
76	rental	0043_remove_fieldresponse_checked_alter_note_file	2024-11-03 00:49:09.380807+00
77	rental	0044_rename_check_option_fieldresponse_check_option_selected	2024-11-03 00:49:10.794119+00
78	rental	0045_contractformtemplate	2024-11-03 00:49:12.396354+00
79	rental	0046_alter_contractformtemplate_options_and_more	2024-11-03 00:49:13.008682+00
80	rental	0047_contractform	2024-11-03 00:49:14.979409+00
81	rental	0048_alter_contractform_template_contractformfield	2024-11-03 00:49:16.823557+00
82	rental	0049_remove_contractformfield_tenant_and_more	2024-11-03 00:49:18.866339+00
83	rental	0050_contractformfieldresponse	2024-11-03 00:49:20.579169+00
84	rental	0051_alter_contractformfieldresponse_form	2024-11-03 00:49:20.967675+00
85	rental	0052_reminder	2024-11-03 00:49:24.055861+00
86	rental	0053_reminder_reminder	2024-11-03 00:49:25.156499+00
87	sessions	0001_initial	2024-11-03 00:49:26.195824+00
88	token_blacklist	0001_initial	2024-11-03 00:49:28.037724+00
89	token_blacklist	0002_outstandingtoken_jti_hex	2024-11-03 00:49:29.077863+00
90	token_blacklist	0003_auto_20171017_2007	2024-11-03 00:49:30.721169+00
91	token_blacklist	0004_auto_20171017_2013	2024-11-03 00:49:32.486809+00
92	token_blacklist	0005_remove_outstandingtoken_jti	2024-11-03 00:49:33.957578+00
93	token_blacklist	0006_auto_20171017_2113	2024-11-03 00:49:35.067606+00
94	token_blacklist	0007_auto_20171017_2214	2024-11-03 00:49:38.512134+00
95	token_blacklist	0008_migrate_to_bigautofield	2024-11-03 00:49:42.348801+00
96	token_blacklist	0010_fix_migrate_to_bigautofield	2024-11-03 00:49:43.046274+00
97	token_blacklist	0011_linearizes_history	2024-11-03 00:49:43.903413+00
98	token_blacklist	0012_alter_outstandingtoken_user	2024-11-03 00:49:44.839251+00
\.


--
-- Data for Name: django_seeding_appliedseeder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."django_seeding_appliedseeder" ("id") FROM stdin;
TenantSeeder
TenantUserSeeder
RentalPlanSeeder
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."django_session" ("session_key", "session_data", "expire_date") FROM stdin;
ic0e1y6voxc38zkva19ysul4ixoyl2nn	.eJxVjEEOwiAQRe_C2pABCohL956BzEyntmogKe3KeHdD0oVu_3vvv1XGfZvz3mTNy6guyqnT70bITykdjA8s96q5lm1dSHdFH7TpWx3ldT3cv4MZ29xrIAlgLQuDQyNR0hkH41KCiIP4icgEnmx0DMSJrIAXnwAJfDAO1ecL8b84Eg:1t7Oz1:S1b1uw0cS9ncnnzbAEPsXnwy7ydxWDrOMXI-WU01ppk	2024-11-17 01:00:47.577929+00
h1xpvc5kahpoqq6bs8ntk0jvglqrs3uu	.eJxVjEEOwiAQRe_C2pABCohL956BzEyntmogKe3KeHdD0oVu_3vvv1XGfZvz3mTNy6guyqnT70bITykdjA8s96q5lm1dSHdFH7TpWx3ldT3cv4MZ29xrIAlgLQuDQyNR0hkH41KCiIP4icgEnmx0DMSJrIAXnwAJfDAO1ecL8b84Eg:1t7fJR:4pH-KQGlhCJCdns11S794cB2og10l6Yyn9nEhL31ddE	2024-11-17 18:26:57.414553+00
wdo3bywasc2pmjb0m0xwmv3cxmf5jlag	.eJxVjEEOwiAQRe_C2pABCohL956BzEyntmogKe3KeHdD0oVu_3vvv1XGfZvz3mTNy6guyqnT70bITykdjA8s96q5lm1dSHdFH7TpWx3ldT3cv4MZ29xrIAlgLQuDQyNR0hkH41KCiIP4icgEnmx0DMSJrIAXnwAJfDAO1ecL8b84Eg:1t7jsk:TF43s2Z2yLl6hJhR14GYaoGDTXghKkYCtlsem8AKwHM	2024-11-17 23:19:42.698357+00
\.


--
-- Data for Name: rental_tenant; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_tenant" ("id", "email", "name", "isAdmin", "date_joined") FROM stdin;
1	admin@tenant.com	Admin-Tenant	t	2024-11-03 00:57:53.482804+00
2	test@tenant.com	Test-Tenant	f	2024-11-03 00:57:53.482962+00
\.


--
-- Data for Name: rental_form; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_form" ("id", "name", "is_active", "created_at", "tenant_id") FROM stdin;
1	Previo a la renta	t	2024-11-06 21:25:27.876558+00	2
2	Formulario	t	2024-11-17 00:49:11.259523+00	2
3	Formulario	f	2024-11-17 00:49:45.670114+00	2
4	Simple	t	2024-11-17 03:29:44.372998+00	2
\.


--
-- Data for Name: rental_card; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_card" ("id", "name", "form_id") FROM stdin;
26	Luces	1
27	Todo	2
28	Todo	3
29	TODO	4
\.


--
-- Data for Name: rental_field; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_field" ("id", "name", "required", "type", "card_id") FROM stdin;
79	Edad	t	NUMBER	27
80	Nombre	t	TEXT	27
81	Casado	t	SINGLE_CHECK	27
82	Correo	t	EMAIL	27
83	Fecha de nacimiento	t	DATE	27
84	Hora	t	TIME	27
85	Telefono	t	PHONE	27
86	Foto	t	IMAGE	27
87	Firma	t	SIGNATURE	27
88	Edad	t	NUMBER	28
89	Nombre	t	TEXT	28
90	Casado	t	SINGLE_CHECK	28
91	Correo	t	EMAIL	28
92	Fecha de nacimiento	t	DATE	28
93	Hora	t	TIME	28
94	Telefono	t	PHONE	28
95	Foto	t	IMAGE	28
96	Firma	t	SIGNATURE	28
97	Edad	t	NUMBER	29
98	Nombre	t	TEXT	29
99	Aprobado	t	SINGLE_CHECK	29
76	Delanteras	t	IMAGE	26
77	Traseras	t	IMAGE	26
78	Stop	t	SINGLE_CHECK	26
\.


--
-- Data for Name: rental_checkoption; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_checkoption" ("id", "name", "field_id", "type") FROM stdin;
51	Funciona	78	POINT_PASS
52	Roto	78	POINT_FAIL
53	si	81	POINT_PASS
54	no	81	POINT_FAIL
55	si	90	POINT_PASS
56	no	90	POINT_FAIL
57	Si	99	POINT_PASS
58	No	99	POINT_FAIL
\.


--
-- Data for Name: rental_client; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_client" ("id", "name", "email", "phone_number", "tenant_id") FROM stdin;
1	Pepe	ppe@gmail.cu	3058336104	2
\.


--
-- Data for Name: rental_rentalplan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_rentalplan" ("id", "name", "amount", "periodicity", "tenant_id") FROM stdin;
2	Monthly trailer rental	1000	Monthly	1
3	Biweekly trailer rental	500	Biweekly	1
4	Weekly trailer rental	250	Weekly	1
\.


--
-- Data for Name: rental_vehicle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_vehicle" ("id", "type", "year", "make", "trim", "vin", "odometer", "nickname", "spare_tires", "extra_fields", "status", "tenant_id", "model", "is_deleted") FROM stdin;
1	Trailer	2023	BigTex	null	1G1AF1F57A7190000	0	testVehicle	1	\N	Available	2	Flatbed	f
\.


--
-- Data for Name: rental_contract; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_contract" ("id", "creation_date", "active_date", "end_date", "client_id", "tenant_id", "vehicle_id", "rental_plan_id") FROM stdin;
1	2024-11-07 23:37:33.169376+00	\N	\N	1	2	1	3
\.


--
-- Data for Name: rental_tenantuser; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_tenantuser" ("id", "role", "is_default", "tenant_id", "user_id") FROM stdin;
1	Admin	t	2	1
2	Admin	t	1	2
3	Admin	f	1	3
4	Admin	t	2	3
5	Admin	t	2	4
6	Admin	f	1	5
7	Admin	t	2	5
\.


--
-- Data for Name: rental_contractformtemplate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_contractformtemplate" ("id", "created_at", "template", "is_active", "name", "tenant_id", "user_id") FROM stdin;
\.


--
-- Data for Name: rental_contractform; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_contractform" ("id", "created_at", "name", "template_id", "tenant_id", "user_id") FROM stdin;
\.


--
-- Data for Name: rental_contractformfield; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_contractformfield" ("id", "placeholder", "type", "required", "template_id") FROM stdin;
\.


--
-- Data for Name: rental_contractformfieldresponse; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_contractformfieldresponse" ("id", "content", "field_id", "form_id") FROM stdin;
\.


--
-- Data for Name: rental_inspection; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_inspection" ("id", "created_at", "form_id", "tenant_id", "tenantUser_id", "vehicle_id") FROM stdin;
1	2024-11-06 21:26:30.726011+00	1	2	4	1
2	2024-11-17 00:50:05.186526+00	2	2	4	1
3	2024-11-17 03:31:21.926268+00	4	2	7	1
4	2024-11-18 16:48:51.566507+00	2	2	4	1
\.


--
-- Data for Name: rental_fieldresponse; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_fieldresponse" ("id", "note", "created_at", "content", "check_option_selected_id", "field_id", "tenantUser_id", "inspection_id") FROM stdin;
1	\N	2024-11-17 03:31:55.063101+00	30	\N	97	7	3
2	\N	2024-11-17 03:31:55.190121+00	Nombre	\N	98	7	3
3	Casi desaprueba	2024-11-17 03:31:55.376198+00	\N	57	99	7	3
4	\N	2024-11-17 03:35:04.622428+00	30	\N	79	7	2
5	\N	2024-11-17 03:35:04.749401+00	Nombre	\N	80	7	2
6	Me obligaron	2024-11-17 03:35:04.940112+00	\N	53	81	7	2
7	\N	2024-11-17 03:35:05.068708+00	email@example.com	\N	82	7	2
8	\N	2024-11-17 03:35:05.207723+00	2024-11-13	\N	83	7	2
9	\N	2024-11-17 03:35:05.33481+00	13:33	\N	84	7	2
10	\N	2024-11-17 03:35:05.462291+00	+36454545454545	\N	85	7	2
11	\N	2024-11-17 03:35:06.346158+00	inspections/2/image-86.png	\N	86	7	2
12	\N	2024-11-17 03:35:06.793953+00	inspections/2/signature-87.png	\N	87	7	2
\.


--
-- Data for Name: rental_note; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_note" ("id", "subject", "body", "createdDate", "remainder", "file", "contract_id", "user_id") FROM stdin;
\.


--
-- Data for Name: rental_vehicleplate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_vehicleplate" ("id", "is_active", "plate", "assign_date", "dismiss_date", "vehicle_id") FROM stdin;
1	t	4232rewr324	2024-11-05 15:30:55.552304+00	\N	1
\.


--
-- Data for Name: rental_tolldue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_tolldue" ("id", "amount", "stage", "invoice", "invoiceNumber", "createDate", "note", "contract_id", "plate_id") FROM stdin;
\.


--
-- Data for Name: rental_reminder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_reminder" ("id", "status", "important", "title", "content", "remainder", "file", "created_at", "client_id", "contract_id", "created_by_id", "toll_due_id", "vehicle_id", "reminder_id") FROM stdin;
1	Waiting	f	Esta nota es una prueba	<p>Acá está el contenido de la prueba</p>	\N		2024-11-07 21:33:14.477+00	\N	\N	4	\N	1	\N
\.


--
-- Data for Name: rental_stageupdate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_stageupdate" ("id", "date", "reason", "comments", "stage", "contract_id") FROM stdin;
1	2024-11-07 23:37:33.372262+00	\N	\N	Pending	1
2	2024-11-07 23:39:54.354742+00	\N	Ya quedó firmado	Active	1
\.


--
-- Data for Name: rental_tracker; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_tracker" ("id", "name", "created_date", "vehicle_id") FROM stdin;
\.


--
-- Data for Name: rental_trackerheartbeatdata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_trackerheartbeatdata" ("id", "timestamp", "latitude", "longitude", "tracker_id") FROM stdin;
\.


--
-- Data for Name: rental_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_user_groups" ("id", "user_id", "group_id") FROM stdin;
\.


--
-- Data for Name: rental_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_user_user_permissions" ("id", "user_id", "permission_id") FROM stdin;
\.


--
-- Data for Name: rental_vehiclepicture; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."rental_vehiclepicture" ("id", "image", "pinned", "vehicle_id") FROM stdin;
\.


--
-- Data for Name: token_blacklist_outstandingtoken; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."token_blacklist_outstandingtoken" ("id", "token", "created_at", "expires_at", "user_id", "jti") FROM stdin;
1	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTM1OTYwMCwiaWF0IjoxNzMwOTI3NjAwLCJqdGkiOiI2ODRiNmExOWFmMzQ0MmM2OTU2MTY4YTAxMGVkMzYyOSIsInVzZXJfaWQiOjN9.4UQl9gODp_vgaYeOtK6eorAtiYJq3D3D3a0bQccWlAk	2024-11-06 21:13:20.679984+00	2024-11-11 21:13:20+00	3	684b6a19af3442c6956168a010ed3629
2	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTQyOTk5MSwiaWF0IjoxNzMwOTk3OTkxLCJqdGkiOiIzY2M5NTVjNGIzMmM0YWVlYWJkYjhkZTlmMjk3ZmU1NCIsInVzZXJfaWQiOjN9.Rt_s3t_v25a8J9YTy1B4TTqgzs_ot63VTX1zO7dzCVE	2024-11-07 16:46:31.503647+00	2024-11-12 16:46:31+00	3	3cc955c4b32c4aeeabdb8de9f297fe54
3	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTQzMDA5MSwiaWF0IjoxNzMwOTk4MDkxLCJqdGkiOiJlNzgzYWRhOTE5YjQ0NjZiOWMwN2I2OTQ4MTRkYjRhNCIsInVzZXJfaWQiOjN9.rUQYD1A2oEH8oU3SuZhLcRyRszQlZ2sptzw7xvvklhw	2024-11-07 16:48:11.101547+00	2024-11-12 16:48:11+00	3	e783ada919b4466b9c07b694814db4a4
4	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTQ0NTY0NywiaWF0IjoxNzMxMDEzNjQ3LCJqdGkiOiJkMjkxZTk4YTk0MTY0MzhmYjA5NmQ0MDU5ZDFhMDFjMyIsInVzZXJfaWQiOjN9.5kAkOTS0E1apTHr57pwfIhclu7h4VS0hl9XWP9y4qmk	2024-11-07 21:07:27.003369+00	2024-11-12 21:07:27+00	3	d291e98a9416438fb096d4059d1a01c3
5	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTQ1NDYyOSwiaWF0IjoxNzMxMDIyNjI5LCJqdGkiOiI0MjQxNzFjYTVlYzM0MjE0YTFmNGIwOGNhNDZkNTJmYyIsInVzZXJfaWQiOjN9.9Ez16-jML5_HFbhajoX_H0uee6jovQuq31jKFk3UaAY	2024-11-07 23:37:09.08042+00	2024-11-12 23:37:09+00	3	424171ca5ec34214a1f4b08ca46d52fc
6	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTkzMTMyNiwiaWF0IjoxNzMxNDk5MzI2LCJqdGkiOiI4ZjAxNjk5OGQwOWE0MmI0YTBiZjg1MDU4NDkxODUyOSIsInVzZXJfaWQiOjN9.f5ndE4vexb7LmeYY_658GpCctxUJlMsbhAfcqQIpAew	2024-11-13 12:02:06.181089+00	2024-11-18 12:02:06+00	3	8f016998d09a42b4a0bf850584918529
7	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMTk1ODA5NSwiaWF0IjoxNzMxNTI2MDk1LCJqdGkiOiIzZDJlMDMyZTA0ZjQ0MDQwODM1MGEwNzFhZTliMGRjMCIsInVzZXJfaWQiOjN9.TpWHa0Tvxqr89BbvCv4Sld5QLQ3KyJsvQfXQbbAt7Z4	2024-11-13 19:28:15.740346+00	2024-11-18 19:28:15+00	3	3d2e032e04f440408350a071ae9b0dc0
8	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjEyODUxOCwiaWF0IjoxNzMxNjk2NTE4LCJqdGkiOiJkNzEzMGY0ZWY4ZDQ0Y2MwYWQ1YzA2OTUzZWY2OTAwMCIsInVzZXJfaWQiOjN9.cUPXotSy_4BnWADRfnGe8ff8zcLaH7XCX9nRn7YCL4o	2024-11-15 18:48:38.038909+00	2024-11-20 18:48:38+00	3	d7130f4ef8d44cc0ad5c06953ef69000
9	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjEzMDA0OSwiaWF0IjoxNzMxNjk4MDQ5LCJqdGkiOiJmYTlkNGVhZGZhZjY0MjRmYjViNDkxYTA3ZjI3ODBjYyIsInVzZXJfaWQiOjR9.7rmBCipN_WiQ0dj3Ekw1dvQ4mVDsiGNuqNpoaJ3rqjE	2024-11-15 19:14:09.62663+00	2024-11-20 19:14:09+00	4	fa9d4eadfaf6424fb5b491a07f2780cc
10	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjEzMDExMSwiaWF0IjoxNzMxNjk4MTExLCJqdGkiOiJjMjhkMTBmMDJiYzk0Y2QyOTIyZDI1NjM0NjIwODJkYSIsInVzZXJfaWQiOjR9.UzXvDiY50BsOzBSIi81Bt9HNlVYd1C1FagyptNR0WsM	2024-11-15 19:15:11.31013+00	2024-11-20 19:15:11+00	4	c28d10f02bc94cd2922d2563462082da
11	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjEzMDE1NiwiaWF0IjoxNzMxNjk4MTU2LCJqdGkiOiIzZWRlZGZlOWE3YzM0NTg2YmNjM2E3ZWQzODVjODAwYyIsInVzZXJfaWQiOjR9.6OmC5COPBxbc7ZW3abzMsvhi0zW3zvtK6n0EcpLvPfs	2024-11-15 19:15:56.283853+00	2024-11-20 19:15:56+00	4	3ededfe9a7c34586bcc3a7ed385c800c
12	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjEzMDY0NCwiaWF0IjoxNzMxNjk4NjQ0LCJqdGkiOiJmOTJjMzc1MGRlOTQ0YjY2OTAzYTlkMjczOWI0NGMwNyIsInVzZXJfaWQiOjN9.2ykMvsoB5zdGDjiH4VwgrLzQeuFKtqdJ3Ho0cpCEWmE	2024-11-15 19:24:04.79195+00	2024-11-20 19:24:04+00	3	f92c3750de944b66903a9d2739b44c07
13	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjEzMTM2OCwiaWF0IjoxNzMxNjk5MzY4LCJqdGkiOiI2YTY2ZjliNDAxZGQ0OTMxODRiZWVjYzIxYjRhZGE4NiIsInVzZXJfaWQiOjN9.toP6-QLBT3NFJNYtXXEUij260MEIkXOxwxxxeFZaQRI	2024-11-15 19:36:08.103895+00	2024-11-20 19:36:08+00	3	6a66f9b401dd493184beecc21b4ada86
14	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjEzMzAzOSwiaWF0IjoxNzMxNzAxMDM5LCJqdGkiOiI3NzFlODk2ZWFjZWM0ZmE1OTRjN2NmM2Q0NzAzMzY3MCIsInVzZXJfaWQiOjN9.2zHIKm_ocGCy0Gd0MulC8H8gdImNY4eYA6de0sXLqXg	2024-11-15 20:03:59.067789+00	2024-11-20 20:03:59+00	3	771e896eacec4fa594c7cf3d47033670
15	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjE1NDU3NiwiaWF0IjoxNzMxNzIyNTc2LCJqdGkiOiIwMWQwYTY0MGQ0Njg0MGNhYmM2MzQzMzliMDgxMDI0YiIsInVzZXJfaWQiOjV9.GKC5hT8GUErJam_hyVXFUCxekh35ioMRzLWZuwF6EZw	2024-11-16 02:02:56.640127+00	2024-11-21 02:02:56+00	5	01d0a640d46840cabc634339b081024b
16	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjE1NDYwMiwiaWF0IjoxNzMxNzIyNjAyLCJqdGkiOiJjMWY2NjJhYTU2MGM0NTUxYTJiNzUxNDY3NTkzNDcxNSIsInVzZXJfaWQiOjN9.RMoQ_zrvFq4KlKKUVZbqVODOP4ujdiHw4O3WI8ewtSE	2024-11-16 02:03:22.098638+00	2024-11-21 02:03:22+00	3	c1f662aa560c4551a2b7514675934715
17	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjIzNjUyOSwiaWF0IjoxNzMxODA0NTI5LCJqdGkiOiIxOWNiZDU0ZTU4ODk0OTQ0YTIwODdkZDc4MzRjMjU0ZCIsInVzZXJfaWQiOjN9.CvOF3GVHOwTF7edFrpHA15gpHJ_xqQI2vkeK0UYkT5g	2024-11-17 00:48:49.297144+00	2024-11-22 00:48:49+00	3	19cbd54e58894944a2087dd7834c254d
18	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjI0NjE0MiwiaWF0IjoxNzMxODE0MTQyLCJqdGkiOiIwMDQwNWJlOTEzMzE0NzQ0YjIwZTA4YTYwOGViMDRkOSIsInVzZXJfaWQiOjV9.oJ5BlYVhK6LSDcUu10Owr6ZBIG9F_EzJlVmDhBT-pyk	2024-11-17 03:29:02.917053+00	2024-11-22 03:29:02+00	5	00405be913314744b20e08a608eb04d9
19	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjM4MDQ3NiwiaWF0IjoxNzMxOTQ4NDc2LCJqdGkiOiIzZTJhOWIzMWQzMjE0MWM1OGFhMDU4ZjM2NTViZjk1NyIsInVzZXJfaWQiOjN9.u7nM_iZzSVYBFUkJXsHbAjGr3UEBRCtuTKFf3HYIBqw	2024-11-18 16:47:56.825851+00	2024-11-23 16:47:56+00	3	3e2a9b31d32141c58aa058f3655bf957
20	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjQ3OTgzNCwiaWF0IjoxNzMyMDQ3ODM0LCJqdGkiOiIxODEzODA2NTliM2Y0OGM0YWYwMzAyN2Y1YjIyMzkxYSIsInVzZXJfaWQiOjR9.2v0FDwaZgrIFzoZchOx_JamrXNViLhZIwDedxbbZ_gw	2024-11-19 20:23:54.941233+00	2024-11-24 20:23:54+00	4	181380659b3f48c4af03027f5b22391a
21	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDU5NTk0MCwiaWF0IjoxNzM0MTYzOTQwLCJqdGkiOiI0OGVjZDU2MWNiNzE0YWI1OWM2MGZhYTM4ZjQ2NDczZCIsInVzZXJfaWQiOjV9.JSFv6iTj-QjJrZka_-Fy0ctPvd0KbyBYtq5WFcrDP7I	2024-12-14 08:12:20.972806+00	2024-12-19 08:12:20+00	5	48ecd561cb714ab59c60faa38f46473d
\.


--
-- Data for Name: token_blacklist_blacklistedtoken; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "public"."token_blacklist_blacklistedtoken" ("id", "blacklisted_at", "token_id") FROM stdin;
\.


--
-- Data for Name: buckets; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."buckets" ("id", "name", "owner", "created_at", "updated_at", "public", "avif_autodetection", "file_size_limit", "allowed_mime_types", "owner_id") FROM stdin;
\.


--
-- Data for Name: objects; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."objects" ("id", "bucket_id", "name", "owner", "created_at", "updated_at", "last_accessed_at", "metadata", "version", "owner_id", "user_metadata") FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."s3_multipart_uploads" ("id", "in_progress_size", "upload_signature", "bucket_id", "key", "version", "owner_id", "created_at", "user_metadata") FROM stdin;
\.


--
-- Data for Name: s3_multipart_uploads_parts; Type: TABLE DATA; Schema: storage; Owner: supabase_storage_admin
--

COPY "storage"."s3_multipart_uploads_parts" ("id", "upload_id", "size", "part_number", "bucket_id", "key", "etag", "owner_id", "version", "created_at") FROM stdin;
\.


--
-- Data for Name: secrets; Type: TABLE DATA; Schema: vault; Owner: supabase_admin
--

COPY "vault"."secrets" ("id", "name", "description", "secret", "key_id", "nonce", "created_at", "updated_at") FROM stdin;
\.


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: auth; Owner: supabase_auth_admin
--

SELECT pg_catalog.setval('"auth"."refresh_tokens_id_seq"', 1, false);


--
-- Name: key_key_id_seq; Type: SEQUENCE SET; Schema: pgsodium; Owner: supabase_admin
--

SELECT pg_catalog.setval('"pgsodium"."key_key_id_seq"', 1, false);


--
-- Name: auditlog_logentry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."auditlog_logentry_id_seq"', 33, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."auth_group_id_seq"', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."auth_group_permissions_id_seq"', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."auth_permission_id_seq"', 136, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."django_admin_log_id_seq"', 7, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."django_content_type_id_seq"', 34, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."django_migrations_id_seq"', 98, true);


--
-- Name: rental_card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_card_id_seq"', 29, true);


--
-- Name: rental_checkoption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_checkoption_id_seq"', 58, true);


--
-- Name: rental_client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_client_id_seq"', 1, true);


--
-- Name: rental_contract_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_contract_id_seq"', 1, true);


--
-- Name: rental_contractform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_contractform_id_seq"', 1, false);


--
-- Name: rental_contractformfield_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_contractformfield_id_seq"', 1, false);


--
-- Name: rental_contractformfieldresponse_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_contractformfieldresponse_id_seq"', 1, false);


--
-- Name: rental_contractformtemplate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_contractformtemplate_id_seq"', 1, false);


--
-- Name: rental_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_field_id_seq"', 99, true);


--
-- Name: rental_fieldresponse_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_fieldresponse_id_seq"', 12, true);


--
-- Name: rental_form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_form_id_seq"', 4, true);


--
-- Name: rental_inspection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_inspection_id_seq"', 4, true);


--
-- Name: rental_note_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_note_id_seq"', 1, false);


--
-- Name: rental_reminder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_reminder_id_seq"', 1, true);


--
-- Name: rental_rentalplan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_rentalplan_id_seq"', 4, true);


--
-- Name: rental_stageupdate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_stageupdate_id_seq"', 2, true);


--
-- Name: rental_tenant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_tenant_id_seq"', 2, true);


--
-- Name: rental_tenantuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_tenantuser_id_seq"', 7, true);


--
-- Name: rental_tolldue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_tolldue_id_seq"', 1, false);


--
-- Name: rental_tracker_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_tracker_id_seq"', 1, false);


--
-- Name: rental_trackerheartbeatdata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_trackerheartbeatdata_id_seq"', 1, false);


--
-- Name: rental_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_user_groups_id_seq"', 1, false);


--
-- Name: rental_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_user_id_seq"', 5, true);


--
-- Name: rental_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_user_user_permissions_id_seq"', 1, false);


--
-- Name: rental_vehicle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_vehicle_id_seq"', 1, true);


--
-- Name: rental_vehiclepicture_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_vehiclepicture_id_seq"', 1, false);


--
-- Name: rental_vehicleplate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."rental_vehicleplate_id_seq"', 1, true);


--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."token_blacklist_blacklistedtoken_id_seq"', 1, false);


--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('"public"."token_blacklist_outstandingtoken_id_seq"', 21, true);


--
-- PostgreSQL database dump complete
--

RESET ALL;
