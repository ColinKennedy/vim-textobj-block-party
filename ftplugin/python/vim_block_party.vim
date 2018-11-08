if !has('python') && !has('python3')
    echoerr "vim-python-function-expander requires Python. Cannot continue loading this plugin"
    finish
endif

if get(g:, 'block_party_loaded', '0') == '1'
    finish
endif


" Get a Python version to run with (Vim 8.0+ can just use `pythonx`)
if get(g:, 'expander_python_version', '2') == '2' && has('python')
   let g:_uspy=":python "
elseif get(g:, 'expander_python_version', '3') == '3' && has('python3')
   let g:_uspy=":python3 "
else
    echoerr "No matching Python version could be found"
endif


function! s:SetupBlockParty()
    execute g:_uspy "from vim_textobj_block_party import environment;environment.init()"
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
