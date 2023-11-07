log_colors_config() {
    local color
    case $1 in
    'DEBUG') color="\e[1;36m" ;;
    'INFO') color="\e[1;32m" ;;
    'WARNING') color="\e[1;33m" ;;
    'ERROR') color="\e[1;31m" ;;
    'CRITICAL') color="\e[31m" ;;
    *) color="\e[0m" ;; # 默认颜色
    esac
    echo -e "$color$2\e[0m"
}

log() {
    local level=$1
    local message=$2
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local colored_message
    log_level="${global_log_level:-DEBUG}"
    colored_message=$(log_colors_config "$level" "$timestamp [$level] $message")

    if [ "$level" == 'DEBUG' ]; then
        if [ "$log_level" == 'DEBUG' ]; then
            echo -e "$colored_message"
        fi
    elif [ "$level" == 'INFO' ]; then
        if [ "$log_level" == 'DEBUG' ] || [ "$log_level" == 'INFO' ]; then
            echo -e "$colored_message"
        fi
    elif [ "$level" == 'WARNING' ]; then
        if [ "$log_level" == 'DEBUG' ] || [ "$log_level" == 'INFO' ] || [ "$log_level" == 'WARNING' ]; then
            echo -e "$colored_message"
        fi
    elif [ "$level" == 'ERROR' ]; then
        if [ "$log_level" == 'DEBUG' ] || [ "$log_level" == 'INFO' ] || [ "$log_level" == 'WARNING' ] || [ "$log_level" == 'ERROR' ]; then
            echo -e "$colored_message"
        fi
    elif [ "$level" == 'CRITICAL' ]; then
        if [ "$log_level" == 'DEBUG' ] || [ "$log_level" == 'INFO' ] || [ "$log_level" == 'WARNING' ] || [ "$log_level" == 'ERROR' ] || [ "$log_level" == 'CRITICAL' ]; then
            echo -e "$colored_message"
        fi
    fi

}

log_d() {
    log 'DEBUG' "$1"
}

log_i() {
    log 'INFO' "$1"
}

log_w() {
    log 'WARNING' "$1"
}

log_e() {
    log 'ERROR' "$1"
}

log_c() {
    log 'CRITICAL' "$1"
}
