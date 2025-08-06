--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Ubuntu 14.18-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.18 (Ubuntu 14.18-0ubuntu0.22.04.1)

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
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.alembic_version (version_num) FROM stdin;
c4ff75a5968e
\.


--
-- Data for Name: buyers; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.buyers (id, username, password, full_name, email, phone, offical_name, signature) FROM stdin;
1	shubham123	e5c423e29a981dd8149066bebe675f3979fb9c7f1cbe97db92604ccbbeba4493	Shubham Verma	shubham.verma@example.com	9876543210	shubham	subh
\.


--
-- Data for Name: sellers; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.sellers (id, username, password, official_name, kyc, seller_rating, since_active) FROM stdin;
1	stylish_seller	dda69783f28fdf6f1c5a83e8400f2472e9300887d1dffffe12a07b92a3d0aa25	Stylish Pvt Ltd	false	0	2025-08-05
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.products (id, product_name, product_code, product_summary, product_description, product_details, product_type, product_category, product_sub_category, brand, gender, age_group, sizes_available, colors_available, material, pattern, fit_type, occasion, fabric_care, mrp, selling_price, discount, offers, stock_quantity, low_stock_threshold, main_image_url, additional_image_urls, video_url, delivery_charge, cod_available, dispatch_time, max_delivery_days, returnable, return_days, exchange_available, warranty, meta_title, meta_description, search_tags, hsn_code, gst_percentage, country_of_origin, seller_id) FROM stdin;
1	Men's Casual Sneakers	SNK123456	Stylish and comfortable sneakers for men	These sneakers offer great style and comfort, perfect for daily wear or casual outings.	{"weight": "850g", "dimensions": "30x20x10 cm", "material_type": "Canvas", "closure_type": "Lace-Up"}	Footwear	Shoes	Sneakers	Sneako	Men	Adult	["6", "7", "8", "9", "10"]	["White", "Black", "Blue"]	Canvas	Solid	Regular	Casual	Wipe with a clean dry cloth	2999.99	1999.99	33.3	{"festival_offer": "Buy 1 Get 1 Free", "bank_offer": "10% off on HDFC cards"}	50	5	https://example.com/images/sneaker_main.jpg	["https://example.com/images/sneaker_1.jpg", "https://example.com/images/sneaker_2.jpg"]	https://example.com/videos/sneaker_demo.mp4	50	t	1	4	t	10	t	6 months manufacturer warranty	Sneako Casual Sneakers for Men	Buy Men's Sneakers online - Stylish, durable, and perfect for everyday use.	["sneakers", "casual shoes", "men's footwear"]	640419	18	India	1
4	woman's Casual Sneakers	SNK123455	Stylish and comfortable sneakers for men	These sneakers offer great style and comfort, perfect for daily wear or casual outings.	{"weight": "850g", "dimensions": "30x20x10 cm", "material_type": "Canvas", "closure_type": "Lace-Up"}	Footwear	Shoes	Sneakers	Sneako	Men	Adult	["6", "7", "8", "9", "10"]	["White", "Black", "Blue"]	Canvas	Solid	Regular	Casual	Wipe with a clean dry cloth	2999.99	1999.99	33.3	{"festival_offer": "Buy 1 Get 1 Free", "bank_offer": "10% off on HDFC cards"}	50	5	https://example.com/images/sneaker_main.jpg	["https://example.com/images/sneaker_1.jpg", "https://example.com/images/sneaker_2.jpg"]	https://example.com/videos/sneaker_demo.mp4	50	t	1	4	t	10	t	6 months manufacturer warranty	Sneako Casual Sneakers for Men	Buy Men's Sneakers online - Stylish, durable, and perfect for everyday use.	["sneakers", "casual shoes", "men's footwear"]	640419	18	India	1
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.reviews (id, rating, product_id, buyer_id) FROM stdin;
\.


--
-- Data for Name: attachments; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.attachments (id, file_url, review_id) FROM stdin;
\.


--
-- Data for Name: buyer_addresses; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.buyer_addresses (id, buyer_id, address_line, city, state, zip_code, country) FROM stdin;
1	1	221B Baker Street	London	Greater London	NW1	UK
\.


--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.cart_items (id, buyer_id, product_id, quantity) FROM stdin;
\.


--
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.comments (id, buyer_id, product_id, content, rating, created_at, review_id) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.orders (id, buyer_id, total_amount, created_at) FROM stdin;
\.


--
-- Data for Name: order_item; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.order_item (id, order_id, product_id, quantity) FROM stdin;
\.


--
-- Data for Name: payment; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.payment (id, order_id, payment_mode, payment_status, paid_at, amount_paid) FROM stdin;
\.


--
-- Data for Name: seller_addresses; Type: TABLE DATA; Schema: public; Owner: django
--

COPY public.seller_addresses (id, seller_id, address_line, city, state, zip_code, country) FROM stdin;
\.


--
-- Name: attachments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.attachments_id_seq', 1, false);


--
-- Name: buyer_addresses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.buyer_addresses_id_seq', 1, true);


--
-- Name: buyers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.buyers_id_seq', 1, false);


--
-- Name: cart_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.cart_items_id_seq', 1, false);


--
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.comments_id_seq', 1, false);


--
-- Name: order_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.order_item_id_seq', 1, false);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.payment_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.products_id_seq', 13, true);


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.reviews_id_seq', 1, false);


--
-- Name: seller_addresses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.seller_addresses_id_seq', 1, false);


--
-- Name: sellers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: django
--

SELECT pg_catalog.setval('public.sellers_id_seq', 3, true);


--
-- PostgreSQL database dump complete
--

