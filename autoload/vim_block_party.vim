function! vim_block_party#around_deep()
    let l:block_party_temp_var = []

pythonx << EOF
from vim_textobj_block_party import party
party.around_deep('l:block_party_temp_var')
EOF

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#around_deep_two_way()
    let l:block_party_temp_var = []

pythonx << EOF
from vim_textobj_block_party import party
party.around_deep('l:block_party_temp_var', two_way=True)
EOF

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#inside_deep()
    let l:block_party_temp_var = []

pythonx << EOF
from vim_textobj_block_party import party
party.inside_deep('l:block_party_temp_var')
EOF

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#around_shallow()
    let l:block_party_temp_var = []

pythonx << EOF
from vim_textobj_block_party import party
party.around_shallow('l:block_party_temp_var')
EOF

    if len(l:block_party_temp_var) == 0
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#around_shallow_two_way()
    let l:block_party_temp_var = []

pythonx << EOF
from vim_textobj_block_party import party
party.around_shallow('l:block_party_temp_var', two_way=True)
EOF

    if l:block_party_temp_var == []
        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#inside_shallow()
    let l:block_party_temp_var = []

pythonx << EOF
from vim_textobj_block_party import party
party.inside_shallow('l:block_party_temp_var')
EOF

    if l:block_party_temp_var == []

        return 0
    endif

    return ['V', l:block_party_temp_var[0], l:block_party_temp_var[1]]
endfunction


function! vim_block_party#move_inside_shallow()
    let l:block_party_temp_var = []

pythonx << EOF
from vim_textobj_block_party import party
cursor = party.get_next_block()
count = int(vim.eval('v:count1'))
party.inside_shallow('l:block_party_temp_var', cursor=cursor, count=count, include_column=True)
EOF

    if len(l:block_party_temp_var) == 0
        return 0
    endif

    let l:block_party_temp_var = [
        \    l:block_party_temp_var[0][0],
        \    l:block_party_temp_var[0][1] + 1,
        \    l:block_party_temp_var[0][2],
        \    l:block_party_temp_var[0][3],
        \]

    return ['V', l:block_party_temp_var, l:block_party_temp_var]
endfunction
