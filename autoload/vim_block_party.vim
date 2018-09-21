function! vim_block_party#around_deep()
    let g:block_party_temp_var = []

python << EOF
from vim_block_party import party
party.around_deep('g:block_party_temp_var')
EOF

    if g:block_party_temp_var == []
        return 0
    endif

    return ['V', g:block_party_temp_var[0], g:block_party_temp_var[1]]
endfunction


function! vim_block_party#inside_deep()
    let g:block_party_temp_var = []

python << EOF
from vim_block_party import party
party.inside_deep('g:block_party_temp_var')
EOF

    if g:block_party_temp_var == []
        return 0
    endif

    return ['V', g:block_party_temp_var[0], g:block_party_temp_var[1]]
endfunction


function! vim_block_party#around_shallow()
    let g:block_party_temp_var = []

python << EOF
from vim_block_party import party
party.around_shallow('g:block_party_temp_var')
EOF

    if len(g:block_party_temp_var) == 0
        return 0
    endif

    return ['V', g:block_party_temp_var[0], g:block_party_temp_var[1]]
endfunction


function! vim_block_party#inside_shallow()
    let g:block_party_temp_var = []

python << EOF
from vim_block_party import party
party.inside_shallow('g:block_party_temp_var')
EOF

    if g:block_party_temp_var == []
        return 0
    endif

    return ['V', g:block_party_temp_var[0], g:block_party_temp_var[1]]
endfunction
