#!/usr/bin/env bash
# Phase 25/26 — one-command reproduction of the ESWA extended evaluation (audit H9).
# Deterministic: PYTHONHASHSEED=0 and every script pins seed=42. Runs from repo root.
# Regenerates backend/reports/extended_evaluation/*.json and research/results/*.json.
#
# Usage:   bash scripts/reproduce_all.sh
# Notes:   - Needs backend/.venv (see backend/requirements-min.txt AND backend/requirements-research.txt,
#            which pins scikit-learn/scipy/xgboost/matplotlib used by the evaluation scripts).
#          - The duplicate-15-jobs scalability micro-benchmark is OPT-IN (RUN_SCALABILITY=1); it is
#            non-defensible (audit) and is superseded by EXP-016. Left off by default so this never wedges.
#          - EXP-018 (LLM-assisted labels) is SEPARATE: it needs local `claude -p` and is not part of the
#            deterministic core. Run it explicitly: .venv/bin/python ../research/experiments/llm_label_expansion.py
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../backend"
PY="./.venv/bin/python"
# Single-thread the numeric/tokenizer stacks: on a loaded machine, torch/tokenizers otherwise
# block at 0% CPU on startup (observed hang). This makes runs deterministic-and-reliable.
export PYTHONHASHSEED=0 PYTHONPATH=. OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false
R="../research/experiments"

run() { echo; echo "=== $1 ==="; shift; "$@"; }

run "EXP-011 extended_evaluation core (kfold, pointwise-LTR, held-out calibration, counterfactual-50, parser, cold-start)" \
    $PY benchmarks/extended_evaluation.py
run "EXP-012 job-held-out generalization (RQ7)"        $PY "$R/job_heldout.py"
run "EXP-013 leave-one-channel-out ablation (RQ2)"     $PY "$R/leave_one_out_ablation.py"
run "EXP-014a LambdaMART baseline (RQ1)"               $PY "$R/lambdamart_baseline.py"
run "EXP-014b JobBERT domain-encoder baseline (RQ1)"   $PY "$R/jobbert_baseline.py"
run "EXP-015 weight-stability bootstrap (RQ2)"         $PY "$R/weight_stability.py"
run "EXP-019 architecture-value characterization (RQ8)" $PY "$R/architecture_value.py"
run "EXP-020 calibration discrimination (RQ3)"         $PY "$R/calibration_discrimination.py"
run "EXP-022 reproducible significance + Holm (RQ1)"    $PY "$R/significance_corrected.py"
# --- Stage-2 strengthening (EXP-023..033). EXP-023 (synthetic corpus) MUST run first: EXP-024/030 read it.
run "EXP-023 synthetic corpus generation (§F-G)"        $PY "$R/synthetic/generate_synthetic.py"
run "EXP-024 structure recovery on synthetic (§F-H)"    $PY "$R/synthetic/structure_recovery.py"
run "EXP-024b non-additive latent recovery control"     $PY "$R/synthetic/structure_recovery_nonadditive.py"
run "EXP-025 protocol-gated model-selection search (§D-E)" $PY "$R/model_selection/search.py"
run "EXP-026 calibration methods, defined target (§N)"  $PY "$R/calibration_methods.py"
run "EXP-027 generalization: unseen cand/job/both (§J)" $PY "$R/generalization.py"
run "EXP-028 explanation faithfulness, mechanistic (§O)" $PY "$R/explanation_faithfulness.py"
run "EXP-029 robustness matrix (§R)"                    $PY "$R/robustness_matrix.py"
run "EXP-030 temporal drift, simulated (§S)"            $PY "$R/temporal_drift.py"
run "EXP-033 failure-injection matrix (§V)"             $PY "$R/failure_injection.py"
run "EXP-034 graded skill-semantics matcher + benchmark (P1)"      $PY "$R/skill_semantics.py"
run "EXP-034b de-circularized skill benchmark + hard negatives"    $PY "$R/skill_semantics_objective.py"
run "EXP-035/036 derived features + fusion on synthetic (P2/P3)"   $PY "$R/synthetic/feature_fusion_synth.py"
run "EXP-043/044 graded skill channel + by-construction audit"     $PY "$R/graded_skill_channel.py"
run "auto-generate manuscript tables from artifacts (§AA/28)" $PY "$R/generate_manuscript_tables.py"
run "regenerate held-out reliability figure fig4 (§30)"       $PY "$R/make_reliability_fig.py"
run "acceptance checks (weight-sum / decomposition / leakage)" $PY "$R/verify_checks.py"
run "numerical consistency check vs manuscript (§AB/29)" $PY "$R/verify_paper_numbers.py"

echo
echo "=== DONE ==="
echo "Artifacts: backend/reports/extended_evaluation/*.json and research/results/*.json"
echo "Scalability (opt-in): RUN_SCALABILITY=1 $PY benchmarks/extended_evaluation.py"
echo "LLM labels (separate, needs claude -p): $PY $R/llm_label_expansion.py"
