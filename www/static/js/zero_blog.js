// zero_blog.js
// copy from awesome.js

// patch for lower-version IE:
if (! window.console) {
    window.console = {
        log: function() {},
        info: function() {},
        error: function() {},
        warn: function() {},
        debug: function() {}
    };
}

// patch for string.trim()

if (! String.prototype.trim) {
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g);
    };
}

if (! Number.prototype.toDateTime) {
    var replaces = {
        'yyyy': function(dt) {
            return dt.getFullYear().toString();
        },
        'yy': function(dt) {
            return (dt.getFullYear() % 100).toString();
        },
        'MM': function(dt) {
            var m = dt.getMonth() + 1;
            return m < 10 ? '0' + m : m.toString();
        },
        'dd': function(dt) {
            var d = dt.getDate();
            return d < 10 ? '0' + d : d.toString();
        },
        'd': function(dt) {
            var d = dt.getDate();
            return d.toString();
        },
        'hh': function(dt) {
            var h = dt.getHours();
            return h < 10 ? '0' + h : h.toString();
        },
        'h': function(dt) {
            var h = dt.getHours();
            return h;
        },
        'mm': function(dt) {
            var m = dt.getMinutes();
            return m < 10 ? '0' + m : m.toString();
        },
        'm': function(dt) {
            var m = dt.getMinutes();
            return m.toString();
        },
        'ss': function(dt) {
            var s = dt.getSeconds();
            return s < 10 ? '0' + s : s.toString();
        },
        's': function(dt) {
            var s = dt.getSeconds();
            return s.toString();
        },
        'a': function(dt) {
            var h = dt.getHours();
            return h < 12 ? 'AM' : 'PM';
        }
    };

    var token = /([a-zA-z]+)/;
    Number.prototype.toDateTime = function(format) {
        var fmt = format || 'yyyy-MM-dd hh:mm:ss';
        var dt = new Date(this * 1000);
        var arr = fmt.split(token);
        for (var i=0; i < arr.length; i++) {
            var s = arr[i];
            if (s && s in replaces) {
                arr[i] = replaces[s](dt);
            }
        }
        return arr.join('');
    };
}


function encodeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/'</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function parseQueryString() {
    var q = location.search, r = {}, i, pos, s, qs;

    if (q && q.charAt(0)==='?') {
        qs = q.substring(1).split('&');
        for (i=0; i<qs.length; i++) {
            s = qs[i];
            pos = s.indexOf('=');
            if (pos <= 0) {
                continue;
            }
            r[s.substring(0, pos)] = decodeURIComponent(s.substring(pos+1)).replace(/\+/g, ' ');
        }
    }
    return r;
}

function gotoPage(i) {
    var r = parseQueryString();
    r.page = i;
    location.assign('?' + $.param(r));
}

function refresh() {
    var t = new Date().getTime(), url = location.pathname;
    if (location.search) {
        url = url + location.search + '&t=' + t;
    } else {
        url = url + '?t' + t;
    }
    location.assign(url);
}

function toSmartDate(timestamp) {
    if (typeof(timestamp) === 'string') {
        timestamp = parseInt(timestamp);
    }
    if (isNan(timestamp)) {
        return '';
    }

    var
    today = new Date(g_time),
    now = todday.getTime(),
    s='1分钟前',
    t = now - timestamp;

    if (t > 604800000) {
        // a week ago:
        var that = new Date(timeStamp);
        var y = that.getFullYear(),
            m = that.getMonth() + 1,
            d = that.getDate(),
            hh = that.getHours(),
            mm = that.getMinutes();
        s = y === today.getFullYear() ? '' : y + '年';
        s = s + m + '月' + d + '日' + 'hh' + ':' + (mm < 10 ? '0' : '') + mm;
    } else if (t >= 86400000) {
        // 1-6 days ago
        s = Math.floor(t / 86400000) + '天前';
    } else if (t >= 3600000) {
        s = Math.floor(t / 3600000) + '小时前';
    } else if (t >= 60000) {
        s = Math.floor(t / 60000) + '分钟前';
    }
    return s;
}

$(function() {
    $('.x-smartdate').each(function() {
        $(this).removeClass('x-smartdate').text(toSmartDate($(this).attr('date')));
    });
});
// JS Template:

function Template(tpl) {
    var fn,
        match,
        code = ['var r=[];\nvar _html = function (str) { return str.replace(/&/g, \'&amp;\').replace(/"/g, \'&quot;\').replace(/\'/g, \'&#39;\').replace(/</g, \'&lt;\').replace(/>/g, \'&gt;\'); };'],
        re = /\{\s*([a-zA-Z\.\_0-9()]+)(\s*safe)?\s*\}/m,
        addLine = function(test) {
            code.push('r.push(\'' + text.replace(/\'/g, '\\\'').replace(/\n/g, '\\n').replace(/\r/g, '\\r') + '\');');
        };
    while (match = re.exec(tpl)) {
        if (match.index > 0) {
            addLine(tpl.slice(0, match.index));
        }
        if (match[2]) {
            code.push('r.push(String(this.' + match[1] + '));');
        } else {
            code.push('r.push(_html(String(this.' + match[1] + ')));');
        }
        tpl = tpl.substring(match.index + match[0].length);
    }
    addLine(tpl);
    code.push('return r.join(\'\');');
    fn = new Function(code.join('\n'));
    this.render = function (model) {
        return fn.apply(model);
    };
}

// extends jQuery.form:

$(function () {
    console.log('Extends $form...');
    $.fn.extend({
        showFormError: function (err) {
            return this.each(function() {
                var
                $form = $(this),
                $alert = $form && $form.find('.uk-alert-danger'),
                fieldName = err && err.data;
                if (! $form.is('form')) {
                    console.error('Cannot call showFormError() on non-form object.');
                    return;
                }

                $form.find('input').removeClass('uk-form-danger');
                $form.find('select').removeClass('uk-form-danger');
                $form.find('textarea').removeClass('uk-form-danger');
                if ($alert.length === 0) {
                    console.warn('Cannot find .uk-alert-danger element.');
                    return;
                }

                if (err) {
                    $alert.text(err.message ? err.message: (err.error ? err.error : err)).removeClass('uk-hidden').show();
                    if (($alert.offset().top - 60) < $(window).scrollTop()) {
                        $('html, body').animate({ scrollTop: $alert.offset().top - 60 });
                    }
                    if (fieldName) {
                        $form.find('[name =' + fieldName + ']').addClass('uk-form-danger');
                    }
                } else {
                    $alert.addClass('uk-hidden').hide();
                    $form.find('.uk-form-danger').removeClass('uk-form-danger');
                }
            });
        },
        showFormLoading: function (isLoading) {
            return this.each(function () {
                var
                $form = $(this),
                $submit = $form && $form.find('button[type=submit]'),
                $buttons = $form && $form.find('button');
                $i = $submit && $submit.find('i'),
                iconClass = $i && $i.attr('class');

                if (! $form.is('form')) {
                    console.error('Cannot call showFormLoading() on non-form object.');
                    return;
                }

                if (!iconClass || iconClass.indexOf('uk-icon') < 0) {
                    console.warn('Icon <i class="uk-icon-*>" not found.');
                    return;
                }
                if (isLoading) {
                    $buttons.attr('disabled', 'disabled');
                    $i && $i.addClass('uk-icon-spinner').addClass('uk-icon-spin');
                } else {
                    $buttons.removeAttr('disabled');
                    $i && $i.removeClass('uk-icon-spinner').remove('uk-icon-spin');
                }
            });
        },
        postJSON: function (url, data, callback) {
            if (arguments.length === 2) {
                callback = data;
                data = {};
            }

            return this.each(function () {
                var $form = $(this);
                $form.showFormError();
                $form.showFormLoading(true);
                _httpJSON('POST', url, data, function (err, r) {
                    if (err) {
                        $form.showFormError(err);
                        $form.showFormLoading(false);
                    }
                    callback && callback(err, r);
                });
            });
        }
    });
});

// ajax submit form:
function _httpJSON(method, url, data, callback) {
    var opt = {
        type: method,
        dataType: 'json'
    };
    if (method === 'GET') {
        opt.url = url + '?' + data;
    }
    if (method === 'POST') {
        opt.url = url;
        opt.data = JSON.stringify(data || {});
        opt.contentType = 'application/json';
    }

    $.ajax(opt).done(function (r) {
        if (r && r.error) {
            return callback(r);
        }
        return callback(null, r);
    }).fail(function (jqXHR, textStatus) {
        return callback({'error': 'http_bad_response', 'data': '' + jqXHR.status, 'message': '网络异常 (HTTP ' + jqXHR.status + ')'});
    });
}
