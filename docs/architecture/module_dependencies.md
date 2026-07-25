# اعتماديات الوحدات النمطية (Module Dependencies)

يوضح هذا المخطط الاعتماديات الرئيسية بين الوحدات النمطية المختلفة في نظام AITOS-v1. تهدف هذه الوثيقة إلى توفير فهم واضح لكيفية تفاعل المكونات مع بعضها البعض.

```mermaid
graph TD
    subgraph Data Acquisition & Processing
        DE[DataEngine]
        MS[Microstructure]
        OF[OrderFlow]
        VP[VolumeProfile]
        ME[MacroEconomics]
    end

    subgraph Analysis & Strategy
        CTA[ClassicalTechnicalAnalysis]
        WY[Wyckoff]
        SMC[Smart Money Concepts]
        ML[MachineLearning]
    end

    subgraph Core Trading Logic
        AE[Alpha Engine]
        RE[RiskEngine]
        RM[RiskManagement]
        PE[PortfolioEngine]
        EE[ExecutionEngine]
        BTE[BacktestEngine]
    end

    DE --> MS
    DE --> OF
    DE --> VP
    DE --> ME

    MS --> CTA
    OF --> CTA
    VP --> CTA

    CTA --> WY
    WY --> SMC

    MS --> ML
    OF --> ML
    VP --> ML
    ME --> ML
    CTA --> ML
    WY --> ML
    SMC --> ML

    SMC --> AE
    ML --> AE

    AE --> RE
    RE --> RM
    AE --> PE
    PE --> RE

    RM --> EE
    RE --> EE

    BTE --> DE
    BTE --> AE
    BTE --> EE
```

**ملاحظة:** هذا المخطط يمثل نظرة عامة على الاعتماديات. قد تكون هناك تفاعلات أكثر تفصيلاً داخل كل وحدة أو بين الوحدات الفرعية.
