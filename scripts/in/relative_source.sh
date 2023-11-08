relative_source() {
  if [[ "$1" =~ / ]]; then
    pushd "$(dirname "$1")" > /dev/null
    . "$(basename "$1")"
    popd > /dev/null
  else
    . "$1"
  fi
}