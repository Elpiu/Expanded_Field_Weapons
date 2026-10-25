-- ============================================================================
-- EFW - OTTIMIZZAZIONE FPS
-- Valori adattati da "FPS BOOSTER" (Workshop 3765424442), corretti per 1.19:
--  * i define grafici stanno in NDefines_Graphics (NDefines.NGraphics non esiste
--    e manderebbe in errore tutto il file Lua);
--  * EVENT_PROCESS_OFFSET sta in NCountry, i *_DIVISION_FACTOR in NAirGfx,
--    MAX_STATE_TARGETS_TO_EVALUATE_PER_HOUR in NRaids.
-- Per disattivare l'ottimizzazione basta cancellare questo file.
-- ============================================================================

-- ---------------------------------------------------------------------------
-- LOG E STORICO (meno memoria occupata nelle partite lunghe)
-- ---------------------------------------------------------------------------
NDefines.NCountry.EVENT_PROCESS_OFFSET = 40                -- Default 20. Controllo eventi distribuito su 40 giorni.
NDefines.NGame.COMBAT_LOG_MAX_MONTHS = 3                   -- Default 12.
NDefines.NGame.LAG_DAYS_FOR_LOWER_SPEED = 25               -- Default 10. Rallenta da velocita 5 piu tardi.
NDefines.NNavy.CONVOY_LOSS_HISTORY_TIMEOUT_MONTHS = 3      -- Default 24.
NDefines.NNavy.NAVAL_COMBAT_RESULT_TIMEOUT_YEARS = 0.25    -- Default 2.
NDefines.NNavy.NAVAL_ACCIDENTS_DAYS_TO_LIVE = 30           -- Default 120.
NDefines.NResistance.GARRISON_LOG_MAX_MONTHS = 3           -- Default 12.
NDefines.NMilitary.GENERATE_AI_DIV_COMMAND_HISTORY_ENTRIES = false -- Default true. Niente storico percorsi divisioni IA.

-- ---------------------------------------------------------------------------
-- IA (calcoli meno frequenti; l'IA si adatta un po' piu lentamente)
-- ---------------------------------------------------------------------------
NDefines.NAI.DAYS_BETWEEN_CHECK_BEST_TEMPLATE = 30         -- Default 7.
NDefines.NAI.DAYS_BETWEEN_CHECK_BEST_DOCTRINE = 90         -- Default 30.
NDefines.NAI.DAYS_BETWEEN_CHECK_BEST_EQUIPMENT = 30        -- Default 7.
NDefines.NAI.RESEARCH_DAYS_BETWEEN_WEIGHT_UPDATE = 20      -- Default 7.
NDefines.NAI.REMOVE_OBSOLETE_TEMPLATE_DAYS = 90            -- Default 180.
NDefines.NAI.REFIT_SHIP_RELUCTANCE = 90                    -- Default 28.
NDefines.NAI.UPGRADE_DIVISION_RELUCTANCE = 14              -- Default 7.
NDefines.NAI.AI_OBJECTIVE_DEFAULT_TARGET_RECALC_DAYS = 7   -- Default 5.
NDefines.NAI.STRIKE_FORCE_TARGET_RECALC_DAYS = 7           -- Default 5.
NDefines.NDiplomacy.DIPLOMACY_HOURS_BETWEEN_REQUESTS = 96  -- Default 24.
NDefines.NRaids.MAX_STATE_TARGETS_TO_EVALUATE_PER_HOUR = 20 -- Default 50.

-- ---------------------------------------------------------------------------
-- GRAFICA
-- ---------------------------------------------------------------------------
NDefines_Graphics.NAirGfx.BOMBERS_DIVISION_FACTOR = 200    -- Default 30. 1 aereo disegnato ogni 200.
NDefines_Graphics.NAirGfx.FIGHTERS_DIVISION_FACTOR = 200   -- Default 30.
NDefines_Graphics.NAirGfx.MISSILES_DIVISION_FACTOR = 200   -- Default 60.
NDefines_Graphics.NAirGfx.TRANSPORT_DIVISION_FACTOR = 200  -- Default 30.

NDefines_Graphics.NGraphics.DRAW_SHADOWS_CUTOFF = 0            -- Default 400. Ombre disattivate.
NDefines_Graphics.NGraphics.TREE_FADE_NEAR = 0                 -- Default 250. Alberi disattivati.
NDefines_Graphics.NGraphics.TREE_FADE_FAR = 0                  -- Default 350.
NDefines_Graphics.NGraphics.UNITS_DISTANCE_CUTOFF = 90         -- Default 120. Modelli 3D -> segnalini prima.
NDefines_Graphics.NGraphics.SHIPS_DISTANCE_CUTOFF = 100        -- Default 240.
NDefines_Graphics.NGraphics.WEATHER_DISTANCE_CUTOFF = 400      -- Default 1500.
NDefines_Graphics.NGraphics.WEATHER_DISTANCE_FADE_LENGTH = 100 -- Default 400.
NDefines_Graphics.NGraphics.DRAW_REFRACTIONS_CUTOFF = 0        -- Default 250. Rifrazioni acqua disattivate.
NDefines_Graphics.NGraphics.MAX_TRAIN_WAGON_COUNT = 3          -- Default 6.
NDefines_Graphics.NGraphics.MAPICON_GROUP_PASSES = 10          -- Default 20.
NDefines_Graphics.NGraphics.TRADE_ROUTE_MAX_LINES = 3          -- Default 6.
NDefines_Graphics.NGraphics.MAP_BUILDINGS_SHRINK_DISTANCE = 0  -- Default 180. Edifici 3D civili disattivati.
NDefines_Graphics.NGraphics.CITY_SPRAWL_SHRINK_DISTANCE = 0    -- Default 220. Espansione urbana disattivata.
NDefines_Graphics.NGraphics.DRAW_FOW_CUTOFF = 0                -- Default 400. Solo l'effetto visivo della nebbia.
NDefines_Graphics.NGraphics.PROVINCE_NAME_DRAW_DISTANCE = 250  -- Default 500.
NDefines_Graphics.NGraphics.GRADIENT_BORDERS_REFRESH_FREQ = 0.30 -- Default 0.12.
NDefines_Graphics.NGraphics.NAVAL_MINES_DISTANCE_CUTOFF = 400  -- Default 800.
