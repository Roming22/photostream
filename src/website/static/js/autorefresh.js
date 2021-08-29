autorefresh = 5000
function AutoRefresh() {
    slideTimeout = setTimeout("location.reload();", autorefresh);
}