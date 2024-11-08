# coding:utf-8

# ---------------------------------------------------------------------------------
# MW-Linux面板
# ---------------------------------------------------------------------------------
# copyright (c) 2018-∞(https://github.com/midoks/mdserver-web) All rights reserved.
# ---------------------------------------------------------------------------------
# Author: midoks <midoks@163.com>
# ---------------------------------------------------------------------------------

import os

from flask import Blueprint, render_template
from flask import request

from admin.model import Sites
from admin.user_login_check import panel_login_required

from utils.plugin import plugin as MwPlugin
from utils.site import sites as MwSites
import utils.site as site
import core.mw as mw
import thisdb

blueprint = Blueprint('site', __name__, url_prefix='/site', template_folder='../../templates/default')
@blueprint.route('/index', endpoint='index')
def index():
    return render_template('site.html')

# 站点列表
@blueprint.route('/list', endpoint='list', methods=['GET','POST'])
@panel_login_required
def list():
    p = request.form.get('p', '1')
    limit = request.form.get('limit', '10')
    type_id = request.form.get('type_id', '0').strip()
    search = request.form.get('search', '').strip()

    info = thisdb.getSitesList(page=int(p),size=int(limit),type_id=int(type_id), search=search)

    data = {}
    data['data'] = info['list']
    data['page'] = mw.getPage({'count':info['count'],'tojs':'getWeb','p':p, 'row':limit})
    return data

# 添加站点
@blueprint.route('/add', endpoint='add',methods=['POST'])
@panel_login_required
def add():
    webname = request.form.get('webinfo', '')
    ps = request.form.get('ps', '')
    path = request.form.get('path', '')
    version = request.form.get('version', '')
    port = request.form.get('port', '')
    return MwSites.instance().add(webname, port, ps, path, version)

# 站点删除
@blueprint.route('/delete', endpoint='delete',methods=['POST'])
@panel_login_required
def delete():
    site_id = request.form.get('id', '')
    path = request.form.get('path', '')
    return MwSites.instance().delete(site_id, path)

# 获取站点类型
@blueprint.route('/get_site_types', endpoint='get_site_types',methods=['POST'])
@panel_login_required
def get_site_types():
    return []

# 获取站点根目录
@blueprint.route('/get_root_dir', endpoint='get_root_dir',methods=['POST'])
@panel_login_required
def get_root_dir():
    data = {}
    data['dir'] = mw.getWwwDir()
    return data

# 获取站点默认文档
@blueprint.route('/get_index', endpoint='get_index',methods=['POST'])
@panel_login_required
def get_index():
    site_id = request.form.get('id', '')
    data = {}
    index = MwSites.instance().getIndex(site_id)
    data['index'] = index
    return data

# 获取站点默认文档
@blueprint.route('/set_index', endpoint='set_index',methods=['POST'])
@panel_login_required
def set_index():
    site_id = request.form.get('id', '')
    index = request.form.get('index', '')
    return MwSites.instance().setIndex(site_id, index)

# 获取站点默认文档
@blueprint.route('/get_limit_net', endpoint='get_limit_net',methods=['POST'])
@panel_login_required
def get_limit_net():
    site_id = request.form.get('id', '')
    return  MwSites.instance().getLimitNet(site_id)

# 获取站点默认文档
@blueprint.route('/set_limit_net', endpoint='set_limit_net',methods=['POST'])
@panel_login_required
def set_limit_net():
    site_id = request.form.get('id', '')
    perserver = request.form.get('perserver', '')
    perip = request.form.get('perip', '')
    limit_rate = request.form.get('limit_rate', '')
    return MwSites.instance().setLimitNet(site_id, perserver,perip,limit_rate)

# 获取站点默认文档
@blueprint.route('/close_limit_net', endpoint='close_limit_net',methods=['POST'])
@panel_login_required
def close_limit_net():
    site_id = request.form.get('id', '')
    return  MwSites.instance().closeLimitNet(site_id)

# 获取站点配置
@blueprint.route('/get_host_conf', endpoint='get_host_conf',methods=['POST'])
@panel_login_required
def get_host_conf():
    siteName = request.form.get('siteName', '')      
    host = MwSites.instance().getHostConf(siteName)
    return {'host': host}


# 获取站点PHP版本
@blueprint.route('/get_site_php_version', endpoint='get_site_php_version',methods=['POST'])
@panel_login_required
def get_site_php_version():
    siteName = request.form.get('siteName', '')      
    return MwSites.instance().getSitePhpVersion(siteName)


# 设置站点PHP版本
@blueprint.route('/set_php_version', endpoint='set_php_version',methods=['POST'])
@panel_login_required
def set_php_version():
    siteName = request.form.get('siteName', '')
    version = request.form.get('version', '') 
    return MwSites.instance().setPhpVersion(siteName,version)

# 检查OpenResty安装/启动状态
@blueprint.route('/check_web_status', endpoint='check_web_status',methods=['POST'])
@panel_login_required
def check_web_status():
    '''
    创建站点检查web服务
    '''
    if not mw.isInstalledWeb():
        return mw.returnJson(False, '请安装并启动OpenResty服务!')

    # 这个快点
    pid = mw.getServerDir() + '/openresty/nginx/logs/nginx.pid'
    if not os.path.exists(pid):
        return mw.returnData(False, '请启动OpenResty服务!')
    return mw.returnData(True, 'OK')

# 获取PHP版本
@blueprint.route('/get_php_version', endpoint='get_php_version',methods=['POST'])
@panel_login_required
def get_php_version():
    return MwSites.instance().getPhpVersion()


# 设置网站到期
@blueprint.route('/set_end_date', endpoint='set_end_date',methods=['POST'])
@panel_login_required
def set_end_date():
    site_id = request.form.get('id', '')
    edate = request.form.get('edate', '')
    return MwSites.instance().setEndDate(site_id, edate)


# 设置网站备注
@blueprint.route('/set_ps', endpoint='set_ps',methods=['POST'])
@panel_login_required
def set_ps():
    site_id = request.form.get('id', '')
    ps = request.form.get('ps', '')
    return MwSites.instance().setPs(site_id, ps)


# 设置默认网站信息
@blueprint.route('/get_default_site', endpoint='get_default_site',methods=['POST'])
@panel_login_required
def get_default_site():
    return MwSites.instance().getDefaultSite()

# 站点删除
@blueprint.route('/get_domain', endpoint='get_domain',methods=['POST'])
@panel_login_required
def get_domain():
    site_id = request.form.get('id', '')
    return MwSites.instance().getDomain(site_id)


@blueprint.route('/set_default_site', endpoint='set_default_site',methods=['POST'])
@panel_login_required
def set_default_site():
    name = request.form.get('name', '')
    return MwSites.instance().setDefaultSite(name)

@blueprint.route('/get_cli_php_version', endpoint='get_cli_php_version',methods=['POST'])
@panel_login_required
def get_cli_php_version():
    php_dir = mw.getServerDir() + '/php'
    if not os.path.exists(php_dir):
        return mw.returnData(False, '未安装PHP,无法设置')

    php_bin = '/usr/bin/php'
    php_versions = MwSites.instance().getPhpVersion()
    php_versions = php_versions[1:]

    if len(php_versions) < 1:
        return mw.returnData(False, '未安装PHP,无法设置')

    if os.path.exists(php_bin) and os.path.islink(php_bin):
        link_re = os.readlink(php_bin)
        for v in php_versions:
            if link_re.find(v['version']) != -1:
                return mw.returnData({"select": v, "versions": php_versions})

    return {"select": php_versions[0],"versions": php_versions}

@blueprint.route('/set_cli_php_version', endpoint='set_cli_php_version',methods=['POST'])
@panel_login_required
def set_cli_php_version():
    if mw.isAppleSystem():
        return mw.returnData(False, "开发机不可设置!")
    version = request.form.get('version', '')
    return MwSites.instance().setCliPhpVersion(version)


