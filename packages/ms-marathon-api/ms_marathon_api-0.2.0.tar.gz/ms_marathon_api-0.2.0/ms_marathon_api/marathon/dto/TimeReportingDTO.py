class TimeReportingDTO:
    def __init__(
        self,
        company,
        employee,
        msemail,
        client,
        clientname,
        project,
        mscode,
        feecode,
        accountingdate,
        recorddate,
        minutes,
    ):
        self.company = company
        self.employee = employee
        self.msemail = msemail
        self.client = client
        self.clientname = clientname
        self.project = project
        self.mscode = mscode
        self.feecode = feecode
        self.accountingdate = accountingdate
        self.recorddate = recorddate
        self.minutes = minutes

    @staticmethod
    def load_data(record):
        def _get_date_isoformat(key_name):
            try:
                return record[key_name].isoformat()
            except Exception:
                return None

        def get_value_as_string(key_name, decode=False):
            try:
                value = record[key_name]
                if value and decode:
                    value = value.decode("utf-8")

                return f"{value}" if value else None
            except Exception:
                return None

        return TimeReportingDTO(
            company=get_value_as_string("company"),
            employee=get_value_as_string("employee"),
            msemail=get_value_as_string("msemail", decode=True),
            client=get_value_as_string("client"),
            clientname=get_value_as_string("clientname"),
            project=get_value_as_string("project"),
            mscode=get_value_as_string("mscode", decode=True),
            feecode=get_value_as_string("feecode"),
            accountingdate=_get_date_isoformat("accountingdate"),
            recorddate=_get_date_isoformat("recorddate"),
            minutes=float(record["minutes"]),
        )

    def to_dict(self):
        return {
            "company": self.company,
            "employee": self.employee,
            "msemail": self.msemail,
            "client": self.client,
            "clientname": self.clientname,
            "project": self.project,
            "mscode": self.mscode,
            "feecode": self.feecode,
            "accountingdate": self.accountingdate,
            "recorddate": self.recorddate,
            "minutes": self.minutes,
        }
