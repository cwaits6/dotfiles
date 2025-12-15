-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua

-- Move code blocks with Shift J+K
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

-- Have deletions go to the d register instead of unamed register
vim.keymap.set("n", "d", '"dd', { noremap = true })
vim.keymap.set("v", "d", '"dd', { noremap = true })
vim.keymap.set("n", "D", '"dD', { noremap = true })
vim.keymap.set("v", "D", '"dD', { noremap = true })

-- Have changes go to the c register instead of unamed register
vim.keymap.set("n", "c", '"cc', { noremap = true })
vim.keymap.set("v", "c", '"cc', { noremap = true })
vim.keymap.set("n", "C", '"cC', { noremap = true })
vim.keymap.set("v", "C", '"cC', { noremap = true })
