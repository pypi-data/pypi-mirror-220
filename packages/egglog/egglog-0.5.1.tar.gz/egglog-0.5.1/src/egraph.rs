// Wrapper around EGraph type

use crate::conversions::*;
use crate::error::EggResult;

use log::info;
use pyo3::prelude::*;
use std::path::PathBuf;

/// EGraph()
/// --
///
/// Create an empty EGraph.
#[pyclass(
    unsendable,
    text_signature = "(*, fact_directory=None, seminaive=True)"
)]
pub struct EGraph {
    egraph: egglog::EGraph,
}

#[pymethods]
impl EGraph {
    #[new]
    #[pyo3(signature = (*, fact_directory=None, seminaive=true))]
    fn new(fact_directory: Option<PathBuf>, seminaive: bool) -> Self {
        let mut egraph = egglog::EGraph::default();
        egraph.fact_directory = fact_directory;
        egraph.seminaive = seminaive;
        Self { egraph }
    }

    /// Parse a program into a list of commands.
    #[pyo3(signature = (input, /))]
    fn parse_program(&mut self, input: &str) -> EggResult<Vec<Command>> {
        info!("Parsing program");
        let commands = self.egraph.parse_program(input)?;
        Ok(commands.into_iter().map(|x| x.into()).collect())
    }

    /// Run a series of commands on the EGraph.
    /// Returns a list of strings representing the output.
    /// An EggSmolError is raised if there is problem parsing or executing.
    #[pyo3(signature=(*commands))]
    fn run_program(&mut self, commands: Vec<Command>) -> EggResult<Vec<String>> {
        let commands: Vec<egglog::ast::Command> = commands.into_iter().map(|x| x.into()).collect();
        info!("Running commands {:?}", commands);
        let res = self.egraph.run_program(commands)?;
        Ok(res)
    }

    /// Gets the last expressions extracted from the EGraph, if the last command
    /// was a Simplify or Extract command.
    #[pyo3(signature = ())]
    fn extract_report(&mut self) -> Option<ExtractReport> {
        info!("Getting last extract report");
        self.egraph
            .get_extract_report()
            .as_ref()
            .map(|report| report.into())
    }

    /// Gets the last run report from the EGraph, if the last command
    /// was a run or simplify command.
    #[pyo3(signature = ())]
    fn run_report(&mut self) -> Option<RunReport> {
        info!("Getting last run report");
        self.egraph
            .get_run_report()
            .as_ref()
            .map(|report| report.into())
    }

    /// Returns the EGraph as graphviz string.
    #[pyo3(signature = ())]
    fn to_graphviz_string(&self) -> String {
        info!("Getting graphviz");
        self.egraph.to_graphviz_string()
    }
}
