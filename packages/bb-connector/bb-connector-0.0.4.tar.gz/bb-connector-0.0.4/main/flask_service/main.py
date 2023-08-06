from xbbg import blp
from entity import bql
from waitress import serve
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response
from exception.handler import handle_bad_request

load_dotenv()

app = Flask(__name__)
app.config.from_envvar("SECRET_KEY_BB_CONNECTOR")
app.register_error_handler(400, handle_bad_request)


@app.route("/bql/primary_exchange_securities", methods=['GET'])
def get_primary_exchange_securities() -> Response:
    """Retrieve all securities which are listed at the requested primary stock exchange.

    Examples
    --------
    {base_url}/bql/primary_exchange_securities?fields=id_isin(),crncy(),security_typ()&security_typ=Common%20Stock&primary_exchange=LN

    :rtype: flask.Response
    :return: BQL-Response
    """

    return bql.BQLQuery(request).retrieve_data_from_excel_app()


@app.route("/bql/fundamental_ticker", methods=['GET'])
def get_fundamental_ticker() -> Response:
    """Retrieve all securities for a primary stock exchange which are also listed at the remote market.

    Examples
    --------
    {base_url}/bql/fundamental_ticker?fields=id_isin(),crncy(),security_typ()&security_typ=Common%20Stock&primary_comp_exchange=LN&exchange=GR

    :rtype: flask.Response
    :return: BQL-Response
    """

    return bql.BQLQuery(request).retrieve_data_from_excel_app()


@app.route("/bql/members", methods=['GET'])
def get_members() -> Response:
    """Retrieve all ETF/Index constituents.

    Examples
    --------
    {base_url}/bql/members?index=OEX%20INDEX

    :rtype: flask.Response
    :return: BQL-Response
    """

    return bql.BQLQuery(request).retrieve_data_from_excel_app()


@app.route("/bdp/field", methods=['GET'])
def get_field() -> Response:
    """Retrieve all ETF/Index constituents.

    Examples
    --------
    {base_url}/bdp/field?ticker=AAPL%20US%20Equity&fields=PX_LAST,PX_VOLUME

    :rtype: flask.Response
    :return: BDP-Response
    """

    bdp_query: str = request.args.get('ticker')
    fields: str | None = request.args.get('fields')
    fields: list[str] = [field.strip() for field in fields.split(',')]

    return jsonify(blp.bdp(bdp_query, fields))


def main():
    serve(app, host='0.0.0.0', port=8080)
