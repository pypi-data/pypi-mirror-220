import os
import time
import pandas as pd
import win32com.client
import flask


class BQLQuery:
    def __init__(self, request: flask.Request):
        self.request = request
        self.query = self.create_query()

    def create_query(self) -> str:
        """Register your endpoints here to call the method"""

        match self.request.path:
            case '/bql/members':
                arg1, arg2 = self._get_members_endpoint()
            case '/bql/primary_exchange_securities':
                arg1, arg2 = self._get_primary_exchange_securities_endpoint()
            case '/bql/fundamental_ticker':
                arg1, arg2 = self._get_fundamental_ticker()
            case _:
                raise NotImplementedError(f'The endpoint {self.request.path} is not yet implemented.')

        # f= is deliberately set so the cell is not yet recognized as an Excel formula
        return f'f=BQL("{arg1}"; "{arg2}"; "Mode=Cached")'

    def _get_primary_exchange_securities_endpoint(self) -> tuple[str, str]:
        primary_exchange = self.request.args.get('primary_exchange')
        exchange = self.request.args.get('exchange')
        security_typ = self.request.args.get('security_typ')
        fields = self.request.args.get('fields')

        for_query_parts = [
            "Filter(EquitiesUniv(['Active']), EXH_CODE=='{primary_exchange}'",
            "and (eqy_prim_security_comp_exch(mode=CACHED) == '{primary_exchange}')",
            "and (exch_code == '{exchange}')",
            "and (security_typ == '{security_typ}'))"
        ]
        for_query = " ".join(for_query_parts).format(
            primary_exchange=primary_exchange,
            exchange=exchange,
            security_typ=security_typ
        )
        return for_query, fields

    def _get_fundamental_ticker(self) -> tuple[str, str]:
        security_typ = self.request.args.get('security_typ')
        primary_comp_exchange = self.request.args.get('primary_comp_exchange')
        exchange = self.request.args.get('exchange')
        fields = self.request.args.get('fields')

        for_query_parts = [
            "fundamentalticker(Filter(EquitiesUniv(['Active']), EXCH_CODE=='{exchange}'",
            "and security_typ == '{security_typ}'",
            "and eqy_prim_security_comp_exch(mode=CACHED) == '{primary_comp_exchange}'))"
        ]
        for_query = " ".join(for_query_parts).format(
            exchange=exchange,
            security_typ=security_typ,
            primary_comp_exchange=primary_comp_exchange
        )
        return for_query, fields

    def _get_members_endpoint(self) -> tuple[str, str]:
        for_query = f"members('{self.request.args.get('index')}')"
        fields = [
            "id_isin()",
            "eqy_prim_security_comp_exch(mode=CACHED)",
            "security_typ()",
            "crncy()",
            "eqy_prim_exch_shrt()"
        ]
        fields = " ".join(fields)
        return for_query, fields

    def retrieve_data_from_excel_app(self) -> flask.Response:
        xlapp = win32com.client.DispatchEx("Excel.Application")

        try:
            xlapp.Workbooks.Open('C:/blp/API/Office Tools/BloombergUI.xla')
        except:
            import sys
            sys.exit()
        support_file = os.path.join(os.environ.get("TEMP_FILE_PATH"), "support_file.xlsx")
        wb = xlapp.workbooks.Add()
        ws = wb.Worksheets(1)
        ws.Name = 'data'

        ws.Cells(1, 1).value = self.query
        ws.Cells(1, 1).Replace('f=', '=')

        wb.RefreshAll()
        xlapp.CalculateUntilAsyncQueriesDone()
        xlapp.DisplayAlerts = False
        time.sleep(os.environ.get("WAITING_TIME", 5))
        wb.SaveAs(support_file)

        xlapp.DisplayAlerts = True
        xlapp.Quit()

        df = pd.read_excel(support_file, sheet_name='data')
        time.sleep(os.environ.get("WAITING_TIME", 5))
        os.remove(support_file)

        return flask.jsonify(df)
