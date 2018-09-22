if get(g:, 'block_party_loaded', '0') == '1'
    finish
endif


function! s:SetupBlockParty()
python << EOF
from vim_textobj_block_party import environment
environment.init()
EOF
endfunction


call s:SetupBlockParty()

call textobj#user#plugin('python', {
\   'block-party-deep': {
\     'select-a-function': 'vim_block_party#around_deep',
\     'select-a': 'aB',
\     'select-i-function': 'vim_block_party#inside_deep',
\     'select-i': 'iB',
\   },
\   'block-party-shallow': {
\     'select-a-function': 'vim_block_party#around_shallow',
\     'select-a': 'ab',
\     'select-i-function': 'vim_block_party#inside_shallow',
\     'select-i': 'ib',
\   },
\   'block-party-two-way': {
\     'select-a-function': 'vim_block_party#around_shallow_two_way',
\     'select-a': 'Ab',
\   },
\ })
