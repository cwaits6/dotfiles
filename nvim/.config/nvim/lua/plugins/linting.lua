return {
  {
    "mfussenegger/nvim-lint",
    event = { "BufWritePost" },
    config = function()
      local lint = require("lint")

      vim.api.nvim_create_autocmd("BufWritePost", {
        pattern = { "*.yaml", "*.yml" },
        callback = function()
          local lines = vim.api.nvim_buf_get_lines(0, 0, 10, false)
          for _, line in ipairs(lines) do
            if line:match("AWSTemplateFormatVersion") then
              lint.try_lint("cfn_lint")
              return
            end
          end
        end,
      })
    end,
  },
}
