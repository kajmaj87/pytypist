autocmd BufWritePre *.py execute ':Black'

map <F2> :wa<CR>:!clear; python pytypist.py<CR>
map <F5> :Black<CR>
map <F8> :wa<CR>:!clear; pytest<CR>
map <F9> :wa<CR>:!clear; pytest -v<CR>
map <F10> :wa<CR>:!clear; pytest -vv<CR>

map <leader>g :YcmCompleter GoTo<CR>
