# config.py

# configuration for game
game = dict(
    width               = 800, # game width
    height              = 800, # game height
    g_name              = "GAME", # game name
    g_time              = 400, # game time
    t_time              = 1000, # game testing time
    fps                 = 60, # frame per second
    delay               = 20, # terminal update delay
    n_best              = 5, # number of best agents
    n_agents            = 50, # number of agents
    s_agent             = 28, # size of an agent
    s_target            = 2, # size of a target
    l_track             = 2., # default speed of left track
    r_track             = 2., # default speed of right track
    r_min               = -0.1, # minimum rotation rate
    r_max               = 0.1, # maximum rotation rate
    agent_startx        = 50,
    agent_starty        = 350,
    n_gates             = 19
)

# configuration for image sources
image = dict(
    icon        = "asset/icon.png", # path of icon image file
    best        = "asset/best.png", # path of best image file
    agent       = "asset/agent.png", # path of agent image file
    target      = "asset/target.png", # path of target image file
)
nnet = dict(
    n_inputs = 5,
    n_outputs = 2,
    n_hidden_layers = 1,
    n_hidden_nodes = [10]
)

gates = ["x30", "x60", "x90", "x120", "x150", "x180", "x210", "x240",
"x270", "x300", "y300", "y270", "y240", "y210", "y180", "y150", "y120",
"y90", "y60"]

ga = dict(
    cx_prob         = .15,
    mut_prob        = .2,
    mate_prob       = .15,
    n_gens          = 30,
    mut_sigma       = 10,
    mut_mu          = 0,
    percent_best    = .05,
    tourn_size      = 5
)
