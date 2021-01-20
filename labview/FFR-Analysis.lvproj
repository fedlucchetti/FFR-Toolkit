<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="17008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Analysis_JSON-v1.vi" Type="VI" URL="../FFRmain/Analysis_JSON-v1.vi"/>
		<Item Name="generate-single-f-control.ctl" Type="VI" URL="../ctl/generate-single-f-control.ctl"/>
		<Item Name="measure.ctl" Type="VI" URL="../ctl/measure.ctl"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Application Directory.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Application Directory.vi"/>
				<Item Name="Close File+.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Close File+.vi"/>
				<Item Name="compatReadText.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatReadText.vi"/>
				<Item Name="DWDT Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/DWDTOps.llb/DWDT Error Code.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Find First Error.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find First Error.vi"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
				<Item Name="NI_AALPro.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALPro.lvlib"/>
				<Item Name="NI_AdvSigProcTFA.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/_Advanced Signal Processing/NI_AdvSigProcTFA.lvlib"/>
				<Item Name="NI_AdvSigProcWA.lvlib" Type="Library" URL="/&lt;vilib&gt;/addons/_Advanced Signal Processing/NI_AdvSigProcWA.lvlib"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="NI_PtbyPt.lvlib" Type="Library" URL="/&lt;vilib&gt;/ptbypt/NI_PtbyPt.lvlib"/>
				<Item Name="Normalize Waveform.vi" Type="VI" URL="/&lt;vilib&gt;/Waveform/WDTOps.llb/Normalize Waveform.vi"/>
				<Item Name="Open File+.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Open File+.vi"/>
				<Item Name="Read Delimited Spreadsheet (DBL).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (DBL).vi"/>
				<Item Name="Read Delimited Spreadsheet (I64).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (I64).vi"/>
				<Item Name="Read Delimited Spreadsheet (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (string).vi"/>
				<Item Name="Read Delimited Spreadsheet.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet.vi"/>
				<Item Name="Read File+ (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read File+ (string).vi"/>
				<Item Name="Read Lines From File (with error IO).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Lines From File (with error IO).vi"/>
				<Item Name="Space Constant.vi" Type="VI" URL="/&lt;vilib&gt;/dlg_ctls.llb/Space Constant.vi"/>
				<Item Name="System Exec.vi" Type="VI" URL="/&lt;vilib&gt;/Platform/system.llb/System Exec.vi"/>
				<Item Name="Write Delimited Spreadsheet (DBL).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (DBL).vi"/>
				<Item Name="Write Delimited Spreadsheet (I64).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (I64).vi"/>
				<Item Name="Write Delimited Spreadsheet (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet (string).vi"/>
				<Item Name="Write Delimited Spreadsheet.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Delimited Spreadsheet.vi"/>
				<Item Name="Write Spreadsheet String.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Write Spreadsheet String.vi"/>
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
			<Item Name="moving average.vi" Type="VI" URL="../DSP/moving average.vi"/>
			<Item Name="scale_waveform.vi" Type="VI" URL="../WaveformOperations/scale_waveform.vi"/>
			<Item Name="SUB CWT.vi" Type="VI" URL="../DSP/SUB CWT.vi"/>
			<Item Name="SUB FFT.vi" Type="VI" URL="../VIs/SUB FFT.vi"/>
			<Item Name="SUB instantant_frequency.vi" Type="VI" URL="../DSP/SUB instantant_frequency.vi"/>
			<Item Name="SUB InstantPhase_v3.vi" Type="VI" URL="../AnalyseFFR/Documents/LABVIEW2014/AnalyseFFR/SUB InstantPhase_v3.vi"/>
			<Item Name="SUB InstPhase_Wavelet.vi" Type="VI" URL="../OnlinePLV/SUB InstPhase_Wavelet.vi"/>
			<Item Name="SUB Json_to_cluster.vi" Type="VI" URL="../DataBase/SUB Json_to_cluster.vi"/>
			<Item Name="SUB measure_Peak2Noise.vi" Type="VI" URL="../DSP/SUB measure_Peak2Noise.vi"/>
			<Item Name="SUB reverse.vi" Type="VI" URL="../WaveformOperations/SUB reverse.vi"/>
			<Item Name="SUB SingleTrialPLV_v03.vi" Type="VI" URL="../AnalyseFFR/Documents/LABVIEW2014/VIs/SUB SingleTrialPLV_v03.vi"/>
			<Item Name="SUB sub_spectrogram.vi" Type="VI" URL="../DSP/SUB sub_spectrogram.vi"/>
			<Item Name="SUB subCWT.vi" Type="VI" URL="../DSP/SUB subCWT.vi"/>
			<Item Name="SUB sum_array.vi" Type="VI" URL="../ArrayOperations/SUB sum_array.vi"/>
			<Item Name="SUB wave2XY.vi" Type="VI" URL="../WaveformOperations/SUB wave2XY.vi"/>
			<Item Name="SUB waveform2XY.vi" Type="VI" URL="../WaveformOperations/SUB waveform2XY.vi"/>
			<Item Name="SUB ZeroPhaseFilter.vi" Type="VI" URL="../AnalyseFFR/Documents/LABVIEW2014/AnalyseFFR/SUB ZeroPhaseFilter.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
