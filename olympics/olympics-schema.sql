--
-- Name: athletes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.athletes (
    id integer,
    athlete_name text
);

--
-- Name: events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.events (
    id integer,
    sport text,
    competition_event text
);

--
-- Name: battleground; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.battleground (
    id integer,
    season text,
    competition_year integer,
    city text
);

--
-- Name: teams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams (
    id integer,
    team text,
    NOC text
);


--
-- Name: event_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_results (
    athlete_id integer,
    athlete_sex text,
    athlete_event_age integer,
    athlete_height integer,
    athlete_weight integer,
    event_id integer,
    battleground_id integer,
    teams_id integer,
    outcome text
);