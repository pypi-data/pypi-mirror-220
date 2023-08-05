from ..data import Data, ic, an, cdt, cst, choices
from ... import enums as enu
from .. import events as ev
from ...types import implementations as impl
from ...version import AppVersion
from ... import ITE_exceptions as exc


class LDN(Data):
    """for ldn"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, impl.octet_string.LDN, classifier=ic.Classifier.STATIC),

    def characteristics_init(self):
        self._cbs_attr_post_init.update(
            {2: lambda: self.collection.set_manufacturer(self.value.contents[:3])}
        )

    @property
    def manufacturer(self) -> bytes:
        return self.value.contents[:3]


class ActiveFirmwareId(Data):
    """for keep version in collection"""
    def characteristics_init(self):
        self._cbs_attr_post_init.update({2: self.__register_value_preset})

    def __register_value_preset(self):
        """need for start control"""
        self.value.register_cb_post_set(self.__handle_value)
        self.__handle_value()

    def __handle_value(self):
        """check new version for more than current collection_version"""
        version = AppVersion.from_str(self.value.contents.decode("utf-8"))
        if (collection_ver := self.collection.server_ver.get(self.logical_name.b)) is not None:
            if version > collection_ver:
                raise exc.NeedUpdate(F"got {version}, but used {collection_ver}. need update server configuration")
            else:
                """ok validation"""
        else:
            """set without check"""


class Unsigned(Data):
    """ with value type: Unsigned """
    A_ELEMENTS = ic.ICAElement(an.VALUE, cdt.Unsigned, classifier=ic.Classifier.DYNAMIC),


class OctetStringDateTime(Data):
    """ with value type: Unsigned """
    A_ELEMENTS = ic.ICAElement(an.VALUE, cst.OctetStringDateTime, classifier=ic.Classifier.DYNAMIC),


class OpeningBody(Data):
    """ RU. 0.0.96.51.0.255. СТО_34.01-5.1-006-2019v3. E 12.1 """
    A_ELEMENTS = ic.ICAElement(an.VALUE, cdt.Unsigned, classifier=ic.Classifier.DYNAMIC),


class SealUnsigned(cdt.Unsigned):
    def get_report(self, with_unit: bool = True) -> str:
        def get_name(value: int):
            """ СПОДЭСv.3 Е.12.5"""
            match value & 0b11:
                case 0: return "Не определено"
                case 1: return "Обжата"
                case 2: return "Взломана"
                case 3: return "Последущие вскрытия"
        return F"Электронные пломбы: корпуса - {get_name(int(self) & 0b11)}, крышки клеммников - {get_name((int(self) >> 2) & 0b11)}"


class SealStatus(Data):
    """ RU. 0.0.96.51.5.255. СТО_34.01-5.1-006-2019v3. E 12.1 """
    A_ELEMENTS = ic.ICAElement(an.VALUE, SealUnsigned, classifier=ic.Classifier.DYNAMIC),


class TerminalsCoverOpeningState(Data):
    """ RU. 0.0.96.51.1.255. СТО_34.01-5.1-006-2019v3. E 12.2 """
    A_ELEMENTS = ic.ICAElement(an.VALUE, cdt.Unsigned, classifier=ic.Classifier.DYNAMIC),


class BitMapData(cdt.Structure):
    start_time: cst.OctetStringDateTime
    stop_time: cst.OctetStringDateTime
    bitmap_data: cdt.OctetString


class ITEBitMap(Data):
    """ITE 0.128.96.13.1.255. Use for send struct lcd screen bitmap(BMP) with start/stop period to server"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, BitMapData, classifier=ic.Classifier.STATIC),


class ChannelNumberValue(cdt.Unsigned):
    @property
    def channel(self) -> enu.ChannelNumber:
        return enu.ChannelNumber(int(self) & 0b0000_0111)

    @channel.setter
    def channel(self, value: enu.ChannelNumber):
        self.set((int(self) & 0b1111_1000) | value)

    @property
    def interface(self) -> enu.Interface:
        return enu.Interface((int(self) & 0b1111_1000) >> 3)

    @interface.setter
    def interface(self, value: enu.Interface):
        self.set((int(self) & 0b0001_1111) | (value << 3))

    def get_report(self, with_unit: bool = True) -> str:
        return F"Номер канала связи: {self.channel.name}, Тип интерфейса: {self.interface.name}"

    def __str__(self):
        return self.report


class CommunicationPortParameter(Data):
    """ RU. 0.0.96.12.4.255. СТО_34.01-5.1-006-2019v3. 13.10. Определение номера порта по которому установлено соединение"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, ChannelNumberValue, default=enu.ChannelNumber.OPTO_P1 + (enu.Interface.OPTO << 3), classifier=ic.Classifier.DYNAMIC),

    @property
    def value(self) -> ChannelNumberValue:
        """override returned type"""
        return self.get_attr(2)


class AnyDateTime(Data):
    """for a-anotation DLMS UA 1000-1 Ed. 14 Table 60"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, choices.any_date_time, classifier=ic.Classifier.STATIC),


class VoltageEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.voltage_events.get_report(int(self))


class SPODES3VoltageEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.2 События, связанные с напряжением"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, VoltageEventValues, classifier=ic.Classifier.STATIC),


class CurrentEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.current_events.get_report(int(self))


class SPODES3CurrentEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.3 События, связанные с током"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, CurrentEventValues, classifier=ic.Classifier.STATIC),


class CommutationEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.commutation_events.get_report(int(self))


class SPODES3CommutationEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.4 События, связанные с вкл./выкл. ПУ, коммутации реле нагрузки"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, CommutationEventValues, classifier=ic.Classifier.STATIC),


class ProgrammingEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.programming_events.get_report(int(self))


class SPODES3ProgrammingEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.5 События программирования параметров ПУ"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, ProgrammingEventValues, classifier=ic.Classifier.STATIC),


class ExternalEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.external_impact_events.get_report(int(self))


class SPODES3ExternalEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.6 События внешних воздействий"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, ExternalEventValues, classifier=ic.Classifier.STATIC),


class CommunicationEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.communication_events.get_report(int(self))


class SPODES3CommunicationEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.7 Коммуникационные события"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, CommunicationEventValues, classifier=ic.Classifier.STATIC),


class AccessEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.access_events.get_report(int(self))


class SPODES3AccessEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.8 События контроля доступа"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, AccessEventValues, classifier=ic.Classifier.STATIC),


class SelfDiagnosticEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.self_diagnostics_events.get_report(int(self))


class SPODES3SelfDiagnosticEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.9 Коды событий для журнала самодиагностики"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, SelfDiagnosticEventValues, classifier=ic.Classifier.STATIC),


class ReactivePowerEventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.reactive_power_events.get_report(int(self))


class SPODES3ReactivePowerEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.10 События по превышению реактивной мощности"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, ReactivePowerEventValues, classifier=ic.Classifier.STATIC),


class PowerQuality2EventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.power_quality_status_2.get_report(int(self))


class SPODES3PowerQuality2Event(Data):
    """СТО_34.01-5.1-006-2019v3 E.1 Статус качества сети (журнал качества сети)"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, PowerQuality2EventValues, classifier=ic.Classifier.STATIC),


class PowerQuality1EventValues(cdt.LongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.power_quality_status_1.get_report(int(self))


class SPODES3PowerQuality1Event(Data):
    """СТО_34.01-5.1-006-2019v3 E.2 Статус качества сети (профиль суточных показаний)"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, PowerQuality1EventValues, classifier=ic.Classifier.STATIC),


# KPZ implements
class KPZ1VoltageEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.voltage_events.get_report(int(self))


class KPZ1SPODES3VoltageEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.2 События, связанные с напряжением with bag in value type"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1VoltageEventValues, classifier=ic.Classifier.STATIC),


class KPZ1CurrentEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.current_events.get_report(int(self))


class KPZ1SPODES3CurrentEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.3 События, связанные с током"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1CurrentEventValues, classifier=ic.Classifier.STATIC),


class KPZ1CommutationEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.commutation_events.get_report(int(self))


class KPZ1SPODES3CommutationEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.4 События, связанные с вкл./выкл. ПУ, коммутации реле нагрузки"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1CommutationEventValues, classifier=ic.Classifier.STATIC),


class KPZ1ProgrammingEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.programming_events.get_report(int(self))


class KPZ1SPODES3ProgrammingEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.5 События программирования параметров ПУ"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1ProgrammingEventValues, classifier=ic.Classifier.STATIC),


class KPZ1ExternalEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.external_impact_events.get_report(int(self))


class KPZ1SPODES3ExternalEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.6 События внешних воздействий"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1ExternalEventValues, classifier=ic.Classifier.STATIC),


class KPZ1CommunicationEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.communication_events.get_report(int(self))


class KPZ1SPODES3CommunicationEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.7 Коммуникационные события"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1CommunicationEventValues, classifier=ic.Classifier.STATIC),


class KPZ1AccessEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.access_events.get_report(int(self))


class KPZ1SPODES3AccessEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.8 События контроля доступа"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1AccessEventValues, classifier=ic.Classifier.STATIC),


class KPZ1SelfDiagnosticEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.self_diagnostics_events.get_report(int(self))


class KPZ1SPODES3SelfDiagnosticEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.9 Коды событий для журнала самодиагностики"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1SelfDiagnosticEventValues, classifier=ic.Classifier.STATIC),


class KPZ1ReactivePowerEventValues(cdt.DoubleLongUnsigned):
    def get_report(self, with_unit: bool = True) -> str:
        return ev.reactive_power_events.get_report(int(self))


class KPZ1SPODES3ReactivePowerEvent(Data):
    """СТО_34.01-5.1-006-2019v3 Д.10 События по превышению реактивной мощности"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, KPZ1ReactivePowerEventValues, classifier=ic.Classifier.STATIC),


class SPODES3SPODESVersionValue(cdt.OctetString):
    def __init__(self, value="332e30"):
        super(SPODES3SPODESVersionValue, self).__init__(value)
        match AppVersion.from_str(self.contents.decode("utf-8")):
            case AppVersion(0, 0, 0): raise ValueError(F"got invalid SPODES VERSION VALUE with: {self}")
            case AppVersion(_, _, None): """valid version"""
            case _: raise ValueError(F"got invalid SPODES VERSION VALUE with: {self}")


class SPODES3SPODESVersion(Data):
    """СТО_34.01-5.1-006-2019v3 Г.1 Примечание 2"""
    A_ELEMENTS = ic.ICAElement(an.VALUE, SPODES3SPODESVersionValue, classifier=ic.Classifier.STATIC),
