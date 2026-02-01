return {
  {
    "neovim/nvim-lspconfig",
    init = function()
      vim.api.nvim_create_autocmd("LspAttach", {
        callback = function(args)
          local client = vim.lsp.get_client_by_id(args.data.client_id)
          if client and client.name == "yamlls" then
            local lines = vim.api.nvim_buf_get_lines(args.buf, 0, 10, false)
            for _, line in ipairs(lines) do
              if line:match("AWSTemplateFormatVersion") then
                vim.schedule(function()
                  vim.lsp.buf_detach_client(args.buf, client.id)
                end)
                return
              end
            end
          end
        end,
      })
    end,
  },
}
