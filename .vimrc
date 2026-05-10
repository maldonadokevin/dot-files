" Leader key
let mapleader = ","

" Line numbers (absolute + relative)
set number relativenumber

" Tabs as 4 spaces
set expandtab tabstop=4 shiftwidth=4

" Search: highlight as you type, case-insensitive unless caps used
set incsearch ignorecase smartcase

" Use system clipboard for yank/paste
set clipboard=unnamed

" No swap files
set noswapfile

" Navigate splits with <leader>hjkl
nnoremap <leader>h <C-w>h
nnoremap <leader>j <C-w>j
nnoremap <leader>k <C-w>k
nnoremap <leader>l <C-w>l

" Clear search highlight
nnoremap <leader><space> :nohlsearch<CR>
