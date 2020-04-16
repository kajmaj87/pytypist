autocmd BufWritePre *.py execute ':Black'

map <F1> :wa<CR><CR>
map <F2> :wa<CR>:!python pytypist.py<CR>
map <F8> :wa<CR>:!pytest<CR>
map <F9> :wa<CR>:!pytest -v<CR>
map <F10> :wa<CR>:!pytest -vv<CR>

map <leader>g :YcmCompleter GoTo<CR>
