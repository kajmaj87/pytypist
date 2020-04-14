autocmd BufWritePre *.py execute ':Black'

map <F2> :wa<CR>:!python pytypist.py<CR>
map <F9> :wa<CR>:!pytest -v<CR>

