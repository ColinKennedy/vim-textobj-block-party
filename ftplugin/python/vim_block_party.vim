if get(g:, 'block_party_loaded', '0') == '1'
    finish
endif


function! s:SetupBlockParty()
pythonx << EOF
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
\   'block-party-deep-two-way': {
\     'select-a-function': 'vim_block_party#around_deep_two_way',
\     'select-a': 'AB',
\   },
\ })


function! s:BlockPartyPrintEnvironment()
    let l:message = "Block Party Version: 1.0.0\n"

    let l:message .= "let g:vim_block_party_greedy = '"
        \ . get(g:, 'vim_block_party_greedy', '0') . "'\n"

    let l:message .= "let g:vim_block_party_include_comments = '"
        \ . get(g:, 'vim_block_party_include_comments', '1') . "'\n"

    let l:message .= "let g:vim_block_party_include_search = '"
        \ . get(g:, 'vim_block_party_include_search', '1') . "'\n"

    let l:message .= "let g:vim_block_party_include_whitespace = '"
        \ . get(g:, 'vim_block_party_include_whitespace', '1') . "'"

    echo l:message
endfunction

command! -buffer BlockPartyDebug call s:BlockPartyPrintEnvironment()


let g:block_party_loaded = '1'
