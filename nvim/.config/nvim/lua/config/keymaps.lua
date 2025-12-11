-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
--
-- Deleted items go to d register instead of unamed register
vim.keymap.set("n", "d", '"dd', { noremap = true })
vim.keymap.set("v", "d", '"dd', { noremap = true })
vim.keymap.set("n", "D", '"dD', { noremap = true })
vim.keymap.set("v", "D", '"dD', { noremap = true })

-- Changed items go to c register instead of unamed register
vim.keymap.set("n", "c", '"cc', { noremap = true })
vim.keymap.set("v", "c", '"cc', { noremap = true })
vim.keymap.set("n", "C", '"cC', { noremap = true })
vim.keymap.set("v", "C", '"cC', { noremap = true })
