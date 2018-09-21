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
\   'block-party-deep': {
\     'select-a-function': 'vim_block_party#around_deep',
\     'select-a': 'ab',
\     'select-i-function': 'vim_block_party#inside_deep',
\     'select-i': 'ib',
\   },
\   'block-party-shallow': {
\     'select-a-function': 'vim_block_party#around_shallow',
\     'select-a': 'aB',
\     'select-i-function': 'vim_block_party#inside_shallow',
\     'select-i': 'iB',
\   },
\   'block-party-deep-no-search': {
\     'select-a-function': 'vim_block_party#around_deep_no_search',
\     'select-a': 'Ab',
\     'select-i-function': 'vim_block_party#inside_deep_no_search',
\     'select-i': 'Ib',
\   },
\   'block-party-shallow-no-search': {
\     'select-a-function': 'vim_block_party#around_shallow_no_search',
\     'select-a': 'AB',
\     'select-i-function': 'vim_block_party#inside_shallow_no_search',
\     'select-i': 'IB',
\   },
\ })
