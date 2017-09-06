binpath='/usr/share/workspaces'
outer_script_path="$binpath/workspaces.sh"
inner_script_path="$binpath/main.py"
alias workspaces="source $outer_script_path"
alias inner_workspaces_script="$inner_script_path"
_workspaces()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts=""

    if [[ ${cur} == * ]] ; then
	opts="`$inner_script_path autocompletionlist` --help -l --list"
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}
complete -F _workspaces workspaces
