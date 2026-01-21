return {
  {
    "folke/snacks.nvim",
    opts = {
      -- File picker options
      picker = {
        sources = {
          explorer = {
            hidden = true,
            auto_close = true,
          },
        },
      },
      -- Enable floating terminal
      terminal = {
        enabled = true,
        win = {
          style = "float",
          border = "rounded",
          width = 0.9,
          height = 0.9,
        },
      },
      -- Custom splash screen logo
      dashboard = {
        preset = {
          header = [[
  ██████   █████ ██████████    ███████    █████   █████ █████ ██████   ██████
  ░░██████ ░░███ ░░███░░░░░█  ███░░░░░███ ░░███   ░░███ ░░███ ░░██████ ██████ 
  ░███░███ ░███  ░███  █ ░  ███     ░░███ ░███    ░███  ░███  ░███░█████░███ 
  ░███░░███░███  ░██████   ░███      ░███ ░███    ░███  ░███  ░███░░███ ░███ 
  ░███ ░░██████  ░███░░█   ░███      ░███ ░░███   ███   ░███  ░███ ░░░  ░███ 
  ░███  ░░█████  ░███ ░   █░░███     ███   ░░░█████░    ░███  ░███      ░███ 
  █████  ░░█████ ██████████ ░░░███████░      ░░███      █████ █████     █████
░░░░░    ░░░░░ ░░░░░░░░░░    ░░░░░░░         ░░░      ░░░░░ ░░░░░     ░░░░░ 


              ]],
        },
      },
    },
    -- Assign keys to open terminal
    keys = {
      {
        "<leader>tt",
        function()
          require("snacks").terminal()
        end,
        desc = "Toggle Snacks Terminal",
      },
    },
  },
}
