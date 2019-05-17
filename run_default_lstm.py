import harness_util

harness_factory = harness_util.TemplateHarnessFactory()

config = {
    'corpusCol': 'description',
    'lstmSize': 64,
    'dropoutRate': 0,
    'kernelRegPenalty': 0.01,
    'method': 'sequence',
    'numWords': 2000,
    'sourceCol': 'source',
    'sourceIdCol': 'sourceId',
    'sourceIdVectorCol': 'sourceIdVector',
    'tokenVectorCol': 'tokenVector',
    'tokensCol': 'tokens',
    'maxSeqLen': 50
}

harness = harness_factory.build(config)

harness.run('who-wrote-this', 'desc-lstm-size-2', config)
