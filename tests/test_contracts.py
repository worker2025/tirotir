from tirotir import Capability, CapabilityError, CapabilityRegistry, Diagnostic, SourceSpan, node_id, v1_contract
from tirotir.core import tokenize

def test_source_span_serialization():
    span=SourceSpan('demo.tirotir',2,3,2,8)
    assert span.to_dict()['start']=={'line':2,'column':3}

def test_diagnostic_serialization():
    d=Diagnostic('TIR1001','error','undefined_name','متغیر پیدا نشد',suggestion='با بگذار تعریف کن')
    value=d.to_dict()
    assert value['code']=='TIR1001' and value['suggestion']

def test_node_id_is_repeatable():
    assert node_id('main.tirotir',4,'Print')==node_id('main.tirotir',4,'Print')

def test_capability_whitelist_defaults_to_core():
    registry=CapabilityRegistry()
    assert registry.allows(Capability.CORE)
    assert not registry.allows(Capability.GUI)
    try: registry.require(Capability.GUI)
    except CapabilityError as error: assert 'gui' in str(error)
    else: raise AssertionError('GUI باید به‌صورت پیش‌فرض مسدود باشد')

def test_v1_contract_is_explicit():
    contract=v1_contract()
    assert contract['language']=='1.1'
    assert contract['unsafe_python_import'] is False

def test_tokens_expose_source_spans():
    token=tokenize('چاپ -سلام-')[0]
    assert token.span.start_line==1 and token.span.start_column==1
