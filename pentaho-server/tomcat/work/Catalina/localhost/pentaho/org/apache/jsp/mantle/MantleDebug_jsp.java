/*
 * Generated by the Jasper component of Apache Tomcat
 * Version: Apache Tomcat/9.0.65
 * Generated at: 2025-06-16 18:16:20 UTC
 * Note: The last modified time of this file was set to
 *       the last modified time of the source file after
 *       generation to assist with modification tracking.
 */
package org.apache.jsp.mantle;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import org.owasp.encoder.Encode;
import org.pentaho.platform.util.messages.LocaleHelper;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Locale;
import java.util.ResourceBundle;

public final class MantleDebug_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {

  private static final javax.servlet.jsp.JspFactory _jspxFactory =
          javax.servlet.jsp.JspFactory.getDefaultFactory();

  private static java.util.Map<java.lang.String,java.lang.Long> _jspx_dependants;

  private static final java.util.Set<java.lang.String> _jspx_imports_packages;

  private static final java.util.Set<java.lang.String> _jspx_imports_classes;

  static {
    _jspx_imports_packages = new java.util.HashSet<>();
    _jspx_imports_packages.add("javax.servlet");
    _jspx_imports_packages.add("javax.servlet.http");
    _jspx_imports_packages.add("javax.servlet.jsp");
    _jspx_imports_classes = new java.util.HashSet<>();
    _jspx_imports_classes.add("java.net.URLClassLoader");
    _jspx_imports_classes.add("org.owasp.encoder.Encode");
    _jspx_imports_classes.add("java.util.ResourceBundle");
    _jspx_imports_classes.add("java.net.URL");
    _jspx_imports_classes.add("java.util.Locale");
    _jspx_imports_classes.add("org.pentaho.platform.util.messages.LocaleHelper");
  }

  private volatile javax.el.ExpressionFactory _el_expressionfactory;
  private volatile org.apache.tomcat.InstanceManager _jsp_instancemanager;

  public java.util.Map<java.lang.String,java.lang.Long> getDependants() {
    return _jspx_dependants;
  }

  public java.util.Set<java.lang.String> getPackageImports() {
    return _jspx_imports_packages;
  }

  public java.util.Set<java.lang.String> getClassImports() {
    return _jspx_imports_classes;
  }

  public javax.el.ExpressionFactory _jsp_getExpressionFactory() {
    if (_el_expressionfactory == null) {
      synchronized (this) {
        if (_el_expressionfactory == null) {
          _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
        }
      }
    }
    return _el_expressionfactory;
  }

  public org.apache.tomcat.InstanceManager _jsp_getInstanceManager() {
    if (_jsp_instancemanager == null) {
      synchronized (this) {
        if (_jsp_instancemanager == null) {
          _jsp_instancemanager = org.apache.jasper.runtime.InstanceManagerFactory.getInstanceManager(getServletConfig());
        }
      }
    }
    return _jsp_instancemanager;
  }

  public void _jspInit() {
  }

  public void _jspDestroy() {
  }

  public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
      throws java.io.IOException, javax.servlet.ServletException {

    if (!javax.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      final java.lang.String _jspx_method = request.getMethod();
      if ("OPTIONS".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        return;
      }
      if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSPs only permit GET, POST or HEAD. Jasper also permits OPTIONS");
        return;
      }
    }

    final javax.servlet.jsp.PageContext pageContext;
    javax.servlet.http.HttpSession session = null;
    final javax.servlet.ServletContext application;
    final javax.servlet.ServletConfig config;
    javax.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    javax.servlet.jsp.JspWriter _jspx_out = null;
    javax.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\n");
      out.write("\n");
      out.write("<!DOCTYPE html>\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");
      out.write("\n");

  // Handle the `locale` request parameter.
  Locale effectiveLocale = LocaleHelper.parseLocale( request.getParameter( "locale" ) );
  LocaleHelper.setSessionLocaleOverride( effectiveLocale );
  LocaleHelper.setThreadLocaleOverride( effectiveLocale );

  effectiveLocale = LocaleHelper.getLocale();

  URLClassLoader loader = new URLClassLoader( new URL[] { application.getResource( "/mantle/messages/" ) } );
  ResourceBundle properties = ResourceBundle.getBundle( "mantleMessages", effectiveLocale, loader );

      out.write("\n");
      out.write("\n");
      out.write("<html>\n");
      out.write("<head>\n");
      out.write("  <title>Pentaho User Console</title>\n");
      out.write("  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\n");
      out.write("  <meta name=\"gwt:property\" content=\"locale=");
      out.print( Encode.forHtmlAttribute(effectiveLocale.toString()) );
      out.write("\">\n");
      out.write("  <link rel=\"icon\" href=\"/pentaho-style/favicon.ico\"/>\n");
      out.write("  <link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/pentaho-style/apple-touch-icon.png\">\n");
      out.write("  <link rel=\"icon\" type=\"image/png\" sizes=\"32x32\" href=\"/pentaho-style/favicon-32x32.png\">\n");
      out.write("  <link rel=\"icon\" type=\"image/png\" sizes=\"16x16\" href=\"/pentaho-style/favicon-16x16.png\">\n");
      out.write("  <link rel=\"mask-icon\" href=\"/pentaho-style/safari-pinned-tab.svg\" color=\"#cc0000\">\n");
      out.write("  <link rel='stylesheet' href='mantle/MantleStyle.css'/>\n");
      out.write("  <link rel=\"stylesheet\" href=\"content/data-access/resources/gwt/datasourceEditorDialog.css\"/>\n");
      out.write("  <link rel=\"stylesheet\" href=\"mantle/Widgets.css\"/>\n");
      out.write("\n");
      out.write("\n");
      out.write("  <script type=\"text/javascript\" src=\"mantle/nativeScripts.js\"></script>\n");
      out.write("  <script type=\"text/javascript\">\n");
      out.write("    /** webcontext.js is created by a PentahoWebContextFilter. This filter searches for an incoming URI having \"webcontext.js\" in it. If it finds that, it write CONTEXT_PATH and FULLY_QUALIFIED_SERVER_URL and it values from the servlet request to this js **/\n");
      out.write("    var CONTEXT_PATH = '/pentaho/';\n");
      out.write("\n");
      out.write("    var FULL_QUALIFIED_URL = 'http://localhost:8080/pentaho/';\n");
      out.write("\n");
      out.write("    var requireCfg = {waitSeconds: 30, paths: {}, shim: {}};\n");
      out.write("    <!-- Injecting web resources defined in by plugins as external-resources for: requirejs-->\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/reporting/reportviewer/reporting-require-js-cfg.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"api/repos/dashboards/script/dashboards-require-js-cfg.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/pentaho-cdf/js/cdf-require-js-cfg.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/pentaho-interactive-reporting/resources/web/pir-require-js-cfg.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/common-ui/resources/web/common-ui-require-js-cfg.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/pentaho-geo/resources/web/geo-require-js-cfg.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/analyzer/scripts/analyzer-require-js-cfg.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"js/require-js-cfg.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script type='text/javascript' src='/pentaho/js/require.js'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script type='text/javascript' src='/pentaho/js/require-cfg.js'></scr\" + \"ipt>\");\n");
      out.write("    <!-- Providing name for session -->\n");
      out.write("    var SESSION_NAME = 'admin';\n");
      out.write("    <!-- Providing computed Locale for session -->\n");
      out.write("    var SESSION_LOCALE = 'en';\n");
      out.write("\n");
      out.write("    <!-- Injecting web resources defined in by plugins as external-resources for: global-->\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/pentaho-mobile/resources/mobile-utils.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/common-ui/resources/web/dojo/djConfig.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/common-ui/resources/web/cache/cache-service.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/common-ui/resources/themes/jquery.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/common-ui/resources/themes/themeUtils.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"js/themes.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    document.write(\"<script language='javascript' type='text/javascript' src='\" + CONTEXT_PATH + \"content/common-ui/resources/themes/jquery.js?context=mantle'></scr\" + \"ipt>\");\n");
      out.write("    var IS_VALID_PLATFORM_LICENSE = true;\n");
      out.write("\n");
      out.write("    if (window.opener && window.opener.reportWindowOpened != undefined) {\n");
      out.write("      window.opener.reportWindowOpened();\n");
      out.write("    }\n");
      out.write("\n");
      out.write("    var dataAccessAvailable = false; //Used by child iframes to tell if data access is available.\n");
      out.write("    /* this function is called by the gwt code when initing, if the user has permission */\n");
      out.write("    function initDataAccess(hasAccess) {\n");
      out.write("      dataAccessAvailable = hasAccess;\n");
      out.write("      if (!hasAccess) {\n");
      out.write("        return;\n");
      out.write("      }\n");
      out.write("      if (typeof(addMenuItem) == \"undefined\") {\n");
      out.write("        setTimeout(\"initDataAccess(\" + hasAccess + \")\", 1000);\n");
      out.write("        return;\n");
      out.write("      } else {\n");
      out.write("        addMenuItem(\"manageDatasourcesEllipsis\", \"manage_content_menu\", \"ManageDatasourcesCommand\");\n");
      out.write("        addMenuItem(\"newDatasource\", \"new_menu\", \"AddDatasourceCommand\");\n");
      out.write("      }\n");
      out.write("    }\n");
      out.write("\n");
      out.write("    var datasourceEditorCallback = {\n");
      out.write("      onFinish: function (val, transport) {\n");
      out.write("      },\n");
      out.write("      onError: function (val) {\n");
      out.write("        alert('error:' + val);\n");
      out.write("      },\n");
      out.write("      onCancel: function () {\n");
      out.write("      },\n");
      out.write("      onReady: function () {\n");
      out.write("      }\n");
      out.write("    }\n");
      out.write("\n");
      out.write("    // This allows content panels to have PUC create new datasources. The iframe requesting\n");
      out.write("    // the new datasource must have a function \"openDatasourceEditorCallback\" on it's window scope\n");
      out.write("    // to be notified of the successful creation of the datasource.\n");
      out.write("    function openDatasourceEditorIFrameProxy(windowReference) {\n");
      out.write("      var callbackHelper = function (bool, transport) {\n");
      out.write("        windowReference.openDatasourceEditorCallback(bool, transport);\n");
      out.write("      }\n");
      out.write("      pho.openDatasourceEditor(new function () {\n");
      out.write("        this.onError = function (err) {\n");
      out.write("          alert(err);\n");
      out.write("        }\n");
      out.write("        this.onCancel = function () {\n");
      out.write("        }\n");
      out.write("        this.onReady = function () {\n");
      out.write("        }\n");
      out.write("        this.onFinish = function (bool, transport) {\n");
      out.write("          callbackHelper(bool, transport);\n");
      out.write("        }\n");
      out.write("      });\n");
      out.write("    }\n");
      out.write("\n");
      out.write("  </script>\n");
      out.write("</head>\n");
      out.write("\n");
      out.write("<body oncontextmenu=\"return false;\" class=\"pentaho-page-background\">\n");
      out.write("\n");
      out.write("<!--\n");
      out.write("	<div id=\"loading\">\n");
      out.write("    		<div class=\"loading-indicator\">\n");
      out.write("    			<img src=\"mantle/large-loading.gif\" width=\"32\" height=\"32\"/>");
      out.print( properties.getString("loadingConsole") );
      out.write("<a href=\"http://www.pentaho.com\"></a><br/>\n");
      out.write("    			<span id=\"loading-msg\">");
      out.print( properties.getString("pleaseWait") );
      out.write("</span>\n");
      out.write("    		</div>\n");
      out.write("	</div>\n");
      out.write("	-->\n");
      out.write("\n");
      out.write("<!-- Standard -->\n");
      out.write("<div id=\"pucWrapper\" cellspacing=\"0\" cellpadding=\"0\" style=\"width: 100%; height: 100%;\">\n");
      out.write("  <div id=\"pucHeader\" cellspacing=\"0\" cellpadding=\"0\">\n");
      out.write("    <div id=\"pucMenuBar\"></div>\n");
      out.write("    <div id=\"pucPerspectives\"></div>\n");
      out.write("    <div id=\"pucToolBar\"></div>\n");
      out.write("    <div id=\"pucUserDropDown\"></div>\n");
      out.write("  </div>\n");
      out.write("\n");
      out.write("  <div id=\"pucContent\"></div>\n");
      out.write("</div>\n");
      out.write("<script type=\"text/javascript\">\n");
      out.write("  document.getElementById(\"pucWrapper\").style.position = \"absolute\";\n");
      out.write("  document.getElementById(\"pucWrapper\").style.left = \"-5000px\";\n");
      out.write("  require([\"common-ui/util/BusyIndicator\"], function (busy) {\n");
      out.write("\n");
      out.write("    busy.show(\"");
      out.print( properties.getString("pleaseWait") );
      out.write("\", \"");
      out.print( properties.getString("loadingConsole") );
      out.write("\", \"pucPleaseWait\");\n");
      out.write("\n");
      out.write("    window.notifyOfLoad = function (area) {\n");
      out.write("      var allFramesLoaded = true;\n");
      out.write("      for (var i = 0; i < window.frames.length; i++) {\n");
      out.write("        if (window.frames[i].document.readyState != \"complete\") {\n");
      out.write("          allFramesLoaded = false;\n");
      out.write("          break;\n");
      out.write("        }\n");
      out.write("      }\n");
      out.write("\n");
      out.write("      if (allFramesLoaded) {\n");
      out.write("        busy.hide(\"pucPleaseWait\");\n");
      out.write("        document.getElementById(\"pucWrapper\").style.left = \"0\";\n");
      out.write("        document.getElementById(\"pucWrapper\").style.position = \"relative\";\n");
      out.write("      } else {\n");
      out.write("        // check again in a bit\n");
      out.write("        setTimeout(\"notifyOfLoad()\", 300);\n");
      out.write("      }\n");
      out.write("    }\n");
      out.write("\n");
      out.write("\n");
      out.write("    // Remove when notifyOfLoad is called from PUC\n");
      out.write("    setTimeout(function () {\n");
      out.write("      notifyOfLoad();\n");
      out.write("    }, 4000);\n");
      out.write("  });\n");
      out.write("\n");
      out.write("</script>\n");
      out.write("\n");
      out.write("<!-- Toolbar On Top -->\n");
      out.write("<!--\n");
      out.write("<table cellspacing=\"0\" cellpadding=\"0\" style=\"width: 100%; height: 100%\">\n");
      out.write("  <tr>\n");
      out.write("    <td id=\"pucToolBar\"></td>\n");
      out.write("  </tr>\n");
      out.write("\n");
      out.write("  <tr>\n");
      out.write("    <td>\n");
      out.write("      <table cellspacing=\"0\" cellpadding=\"0\" >\n");
      out.write("        <tr>\n");
      out.write("          <td id=\"pucMenuBar\" style=\"width:100%\"></td>\n");
      out.write("          <td id=\"pucPerspectives\"></td>\n");
      out.write("        </tr>\n");
      out.write("      </table>\n");
      out.write("    </td>\n");
      out.write("  </tr>\n");
      out.write("\n");
      out.write("  <tr>\n");
      out.write("    <td id=\"pucContent\" style=\"width:100%;height:100%\"></td>\n");
      out.write("  </tr>\n");
      out.write("</table>\n");
      out.write("-->\n");
      out.write("\n");
      out.write("\n");
      out.write("<!-- LOGO -->\n");
      out.write("<!--\n");
      out.write("<table cellspacing=\"0\" cellpadding=\"0\" style=\"width: 100%; height: 100%\">\n");
      out.write("  <tr>\n");
      out.write("    <td colspan=\"2\">\n");
      out.write("      <table cellspacing=\"0\" cellpadding=\"0\" style=\"width: 100%\">\n");
      out.write("        <tr>\n");
      out.write("          <td id=\"pucMenuBar\" style=\"width:100%\"></td>\n");
      out.write("          <td id=\"pucPerspectives\"></td>\n");
      out.write("        </tr>\n");
      out.write("      </table>\n");
      out.write("    </td>\n");
      out.write("  </tr>\n");
      out.write("\n");
      out.write("  <tr>\n");
      out.write("    <td id=\"pucToolBar\"></td>\n");
      out.write("    <td style=\"background-color: white;\">LOGO PANEL</td>\n");
      out.write("  </tr>\n");
      out.write("\n");
      out.write("  <tr>\n");
      out.write("    <td id=\"pucContent\" colspan=\"2\" style=\"width:100%;height:100%\"></td>\n");
      out.write("  </tr>\n");
      out.write("</table>\n");
      out.write("-->\n");
      out.write("\n");
      out.write("\n");
      out.write("<!-- OPTIONAL: include this if you want history support -->\n");
      out.write("<iframe id=\"__gwt_historyFrame\" style=\"width:0px;height:0px;border:0;display:none\"></iframe>\n");
      out.write("\n");
      out.write("</body>\n");
      out.write("\n");
      out.write("<script language='javascript' src='mantle/mantle.nocache.js'></script>\n");
      out.write("\n");
      out.write("</html>\n");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof javax.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
