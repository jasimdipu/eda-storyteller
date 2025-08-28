from __future__ import annotations
from typing import List
from shared.shared.schemas.actions import Actions, Suggestion, CodeSnippet
from shared.shared.schemas.profile import DatasetProfile


def plan_actions(profile: DatasetProfile) -> Actions:
    suggestions: List[Suggestion] = []
    for col, meta in profile.columns.items():
        mr = meta.missing_rate or 0.0
        dt = (meta.dtype or "").lower()
        if mr >= 0.3:
            suggestions.append(Suggestion(type="impute", column=col,
                                          strategy=("median" if "int" in dt or "float" in dt else "most_frequent"),
                                          reason=f"{mr:.0%} missing"))
        elif mr >= 0.1:
            suggestions.append(
                Suggestion(type="impute", column=col, strategy=("median" if "int" in dt or "float" in dt else "mode"),
                           reason=f"{mr:.0%} missing"))
        if (meta.outlier_rate or 0) > 0.05 and ("int" in dt or "float" in dt):
            suggestions.append(Suggestion(type="drop_outliers", column=col, strategy="iqr",
                                          reason=f"{meta.outlier_rate:.0%} outliers"))
        if meta.cardinality and meta.cardinality > 50 and ("cat" in dt or "object" in dt or "str" in dt):
            suggestions.append(Suggestion(type="encode", column=col, strategy="hashing",
                                          reason=f"high cardinality {meta.cardinality}"))

    if profile.quality and (profile.quality.duplicates_rate or 0) > 0.02:
        suggestions.append(Suggestion(type="deduplicate", strategy="drop_duplicates",
                                      reason=f"duplicates {profile.quality.duplicates_rate:.1%}"))

    code: List[CodeSnippet] = []
    for s in suggestions[:6]:
        if s.type == "impute" and s.column:
            body = f"df['{s.column}'] = df['{s.column}'].fillna(df['{s.column}'].median())\n" if s.strategy == "median" else f"df['{s.column}'] = df['{s.column}'].fillna(df['{s.column}'].mode().iloc[0])\n"
        code.append(CodeSnippet(lang="python", stage="cleaning", body=body))
        if s.type == "drop_outliers" and s.column:
            body = (
                "Q1=df['{c}'].quantile(0.25); Q3=df['{c}'].quantile(0.75); IQR=Q3-Q1\nmask=(df['{c}']>=Q1-1.5*IQR)&(df['{c}']<=Q3+1.5*IQR)\ndf=df[mask]\n").replace(
                "{c}", s.column)
        code.append(CodeSnippet(lang="python", stage="cleaning", body=body))
    return Actions(priority="medium", suggestions=suggestions, code_snippets=code)
