" Get a Python version to run with (Vim 8.0+ can just use `pythonx`)
if get(g:, 'expander_python_version', '2') == '2' && has('python')
   let g:_uspy=":python "
elseif get(g:, 'expander_python_version', '3') == '3' && has('python3')
   let g:_uspy=":python3 "
else
    echoerr "No matching Python version could be found"
endif


function! vim_block_party#around_deep()
    let l:block_party_temp_var = []

    execute g:_uspy "from vim_textobj_block_party import party;party.around_deep('l:block_party_temp_var')"

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#around_deep_two_way()
    let l:block_party_temp_var = []

    execute g:_uspy "from vim_textobj_block_party import party;party.around_deep('l:block_party_temp_var', two_way=True)"

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#inside_deep()
    let l:block_party_temp_var = []

    execute g:_uspy "from vim_textobj_block_party import party;party.inside_deep('l:block_party_temp_var')"

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#around_shallow()
    let l:block_party_temp_var = []

    execute g:_uspy "from vim_textobj_block_party import party;party.around_shallow('l:block_party_temp_var')"

    if len(l:block_party_temp_var) == 0
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#around_shallow_two_way()
    let l:block_party_temp_var = []

    execute g:_uspy "from vim_textobj_block_party import party;party.around_shallow('l:block_party_temp_var', two_way=True)"

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#inside_shallow()
    let l:block_party_temp_var = []

    execute g:_uspy "from vim_textobj_block_party import party;party.inside_shallow('l:block_party_temp_var')"

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction
