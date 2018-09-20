if !has('python')
    echoerr "vim-block-party requires Python. Cannot continue loading this plugin"
    finish
endif

if get(g:, 'block_party_loaded', '0') == '1'
    finish
endif


function! s:SetupBlockParty()
python << EOF
from vim_block_party import environment
environment.init()))
EOF
endfunction


let g:block_party_loaded = '1'
