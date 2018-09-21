if get(g:, 'block_party_loaded', '0') == '1'
    finish
endif


function! s:SetupBlockParty()
python << EOF
from vim_block_party import environment
environment.init()
EOF
endfunction


call s:SetupBlockParty()

" TODO : Make these functions in this script only


call textobj#user#plugin('python', {
\   '-': {
\     'select-a-function': 'vim_block_party#around_deep',
\     'select-a': 'aB',
\     'select-i-function': 'vim_block_party#inside_deep',
\     'select-i': 'iB',
\   },
\ })


call textobj#user#plugin('python', {
\   '-': {
\     'select-a-function': 'vim_block_party#around_shallow',
\     'select-a': 'ab',
\     'select-i-function': 'vim_block_party#inside_shallow',
\     'select-i': 'ib',
\   },
\ })
