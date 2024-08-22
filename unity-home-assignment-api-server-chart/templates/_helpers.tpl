{{/*
Return the fully qualified app name.
*/}}
{{- define "unity-home-assignment-api-server-chart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Return the name of the chart.
*/}}
{{- define "unity-home-assignment-api-server-chart.name" -}}
{{- printf "%s" .Chart.Name -}}
{{- end -}}

{{/*
Return the chart version.
*/}}
{{- define "unity-home-assignment-api-server-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version -}}
{{- end -}}
